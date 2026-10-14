package main

import (
	"archive/zip"
	"crypto/sha256"
	"encoding/json/v2"
	"fmt"
	"hash/fnv"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"runtime"
	"slices"
	"strconv"
	"strings"
	"time"

	"github.com/andygrunwald/vdf"
)

type sortType string

const (
	Time sortType = "time"
	Size sortType = "size"
	Name sortType = "name"
)

func getLevelsPath(c Config) string {
	return filepath.Join(c.BeamNGPath, "content", "levels/")
}
func getVehiclesPath(c Config) string {
	return filepath.Join(c.BeamNGPath, "content", "vehicles/")
}

type Config struct {
	DownloadsPath string   `json:"downloadsPath"`
	BeamNGPath    string   `json:"beamngPath"`
	BeamMpPath    string   `json:"beammpPath"`
	SortType      sortType `json:"sortType"`
}
type IgnoreList []string

func downloadIL(hash uint64) bool {
	ignoreListPath := filepath.Join(getAppDirPath(), "ignoreList.txt")
	client := http.Client{Timeout: 10 * time.Second}
	resp, ok := client.Get(sourceURL + "ignoreList.txt")
	if ok != nil {
		return false
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return false
	}
	tmp, err := os.CreateTemp(filepath.Dir(ignoreListPath), "ignoreList-*.tmp")
	if err != nil {
		return false
	}
	defer tmp.Close()
	defer os.Remove(tmp.Name())
	h := fnv.New64a()
	_, ok = io.Copy(io.MultiWriter(h, tmp), resp.Body)
	if ok != nil || h.Sum64() != hash {
		return false
	}
	if err = tmp.Sync(); err != nil {
		return false
	}

	if err = tmp.Close(); err != nil {
		return false
	}
	return os.Rename(tmp.Name(), ignoreListPath) == nil
}
func loadIgnoreList() (ignoreLisT IgnoreList) {
	var ignoreList IgnoreList
	ignoreListPath := filepath.Join(getAppDirPath(), "ignoreList.txt")
	f, err := os.Open(ignoreListPath)
	hil, ok := getILhash()
	if os.IsNotExist(err) {
		if ok == nil {
			if !downloadIL(hil) {
				return make(IgnoreList, 0)
			}
		} else {
			return make(IgnoreList, 0)
		}
		f, err = os.Open(ignoreListPath)
		if err != nil {
			return make(IgnoreList, 0)
		}
		defer f.Close()
	} else if err == nil {
		defer f.Close()
		if ok == nil {
			hilf := fnv.New64a()
			_, ok := io.Copy(hilf, f)
			if ok != nil {
				return make(IgnoreList, 0)
			}
			if hilf.Sum64() != hil {
				f.Close()
				downloadIL(hil)
			}
		}

	} else {
		unwrap(err)
	}
	ilf, err := os.ReadFile(ignoreListPath)
	unwrap(err)
	ignoreList = strings.Split(string(ilf), "\n")
	return ignoreList
}
func getILhash() (uint64, error) {
	client := http.Client{Timeout: 10 * time.Second}
	resp, err := client.Get(sourceURL + ".ILhash")
	if err != nil {
		return 0, err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return 0, fmt.Errorf("%s", resp.Status)
	}
	b, err := io.ReadAll(resp.Body)
	if err != nil {
		return 0, err
	}
	c := string(b)
	h, _, _ := strings.Cut(c, " ")
	return strconv.ParseUint(h, 10, 64)
}
func isFirstRun() bool {
	appDir := getAppDirPath()
	_, err := os.ReadDir(appDir)
	if os.IsNotExist(err) {
		return true
	}
	return false
}
func firstRun() {
	appDir := getAppDirPath()
	err := os.MkdirAll(filepath.Join(appDir, "modpacks/"), 0755)
	unwrap(err)
	defaultModPack(getDatabase(getConfig()))
}
func getConfig() Config {
	var config Config
	configPath := getConfigPath()
	f, err := os.ReadFile(configPath)
	if os.IsNotExist(err) {
		ok := os.MkdirAll(filepath.Dir(configPath), 0755)
		unwrap(ok)
		config = defaultConfig()
		b, ok := json.Marshal(config)
		unwrap(ok)
		ok = os.WriteFile(configPath, b, 0644)
		unwrap(ok)
	} else if err == nil {
		ok := json.Unmarshal(f, &config)
		unwrap(ok)

	} else {
		log.Fatal(err)
	}
	if config.SortType == "" {
		config.SortType = Time
		b, ok := json.Marshal(config)
		unwrap(ok)
		ok = os.WriteFile(configPath, b, 0644)
		unwrap(ok)

	}
	return config
}

type ModType string

const (
	ModVehicle ModType = "vehicle"
	ModMap     ModType = "map"
)

type Mod struct {
	Name    string  `json:"name"`
	Path    string  `json:"path"`
	Size    int     `json:"size"`
	Time    int     `json:"time"`
	Hash    uint64  `json:"hash"`
	Type    ModType `json:"type"`
	Enabled bool    `json:"enabled,omitempty"`
	SHA     string  `json:"sha,omitempty"`
}

func (m *Mod) toggle(state ...bool) {
	if m.Type == ModMap {
		return
	}
	old := m.Path
	if len(state) == 0 {
		if m.Enabled {
			m.toggle(false)
		} else {
			m.toggle(true)
		}
		return
	}
	if m.Enabled == state[0] {
		return
	}
	if !state[0] {
		m.Enabled = false
		m.Path = m.Path + ".dis"
	} else {
		m.Enabled = true
		m.Path = strings.TrimSuffix(m.Path, ".dis")
	}
	err := os.Rename(old, m.Path)
	unwrap(err)
}

type Database struct {
	Mods map[uint64]Mod
}

func (d *Database) createModPack(name string) ModPack {
	var modpack ModPack
	modpack.Name = name
	modpack.EnabledMods = make([]uint64, 0, len(d.Mods))
	for _, mod := range d.listMods("")[ModVehicle] {
		if mod.Enabled {
			modpack.EnabledMods = append(modpack.EnabledMods, mod.Hash)
		}
	}
	modpack.writeModpack()
	return modpack
}
func (d *Database) namesMods() map[string][]Mod {
	mods := make(map[string][]Mod)
	for _, mod := range d.Mods {
		mods[mod.Name] = append(mods[mod.Name], mod)
	}
	return mods
}
func (d *Database) listMods(sortBy sortType) map[ModType][]Mod {
	mods := make(map[ModType][]Mod)
	for _, mod := range d.Mods {
		mods[mod.Type] = append(mods[mod.Type], mod)
	}
	compareMods := func(a, b Mod) int {
		return sortMods(a, b, sortBy)
	}
	slices.SortFunc(mods[ModMap], compareMods)
	slices.SortFunc(mods[ModVehicle], compareMods)
	return mods
}

type ModPack struct {
	Name        string   `json:"name"`
	EnabledMods []uint64 `json:"mods"`
}

func (mp *ModPack) update(d Database) {
	mp.EnabledMods = make([]uint64, 0, len(d.Mods))
	for _, mod := range d.listMods("")[ModVehicle] {
		if mod.Enabled {
			mp.EnabledMods = append(mp.EnabledMods, mod.Hash)
		}
	}
	mp.writeModpack()
}
func (mp *ModPack) delete() error {
	mpPath := filepath.Join(getAppDirPath(), "modpacks/", mp.Name)
	return os.Remove(mpPath)
}
func (mp *ModPack) writeModpack() {
	modPackDir := filepath.Join(getAppDirPath(), "modpacks/")
	err := os.MkdirAll(modPackDir, 0755)
	unwrap(err)
	b, err := json.Marshal(mp)
	unwrap(err)
	err = os.WriteFile(filepath.Join(modPackDir, mp.Name), b, 0644)
	unwrap(err)

}
func (mp *ModPack) loadModPack(d *Database) {
	for _, mod := range d.listMods("")[ModVehicle] {
		if slices.Contains(mp.EnabledMods, mod.Hash) {
			mod.toggle(true)
		} else {
			mod.toggle(false)
		}
		d.Mods[mod.Hash] = mod
	}
	d.writeDatabase()
}
func listModPacks() []ModPack {
	var modpacks []ModPack
	modPackDir := filepath.Join(getAppDirPath(), "modpacks/")
	files, err := os.ReadDir(modPackDir)
	unwrap(err)
	for _, file := range files {
		var modpack ModPack
		modPackPath := filepath.Join(modPackDir, file.Name())
		b, err := os.ReadFile(modPackPath)
		unwrap(err)
		err = json.Unmarshal(b, &modpack)
		unwrap(err)
		modpacks = append(modpacks, modpack)
	}
	return modpacks
}
func mapModPacks() map[string]ModPack {
	mpm := make(map[string]ModPack)
	for _, modPack := range listModPacks() {
		mpm[modPack.Name] = modPack
	}
	return mpm
}
func defaultModPack(d Database) ModPack {
	var modpack ModPack
	modpack.Name = "Default"
	keys := make([]uint64, 0, len(d.Mods))
	for _, mod := range d.listMods("")[ModVehicle] {
		keys = append(keys, mod.Hash)
	}
	modpack.EnabledMods = keys
	modpack.writeModpack()
	return modpack
}
func (d *Database) writeDatabase() {
	databasePath := filepath.Join(getAppDirPath(), "database.json")
	b, err := json.Marshal(d)
	unwrap(err)
	err = os.WriteFile(databasePath, b, 0644)
	unwrap(err)
}
func getDatabase(c Config) Database {
	database := Database{Mods: make(map[uint64]Mod)}
	databasePath := filepath.Join(getAppDirPath(), "database.json")
	f, err := os.ReadFile(databasePath)
	if err == nil {
		ok := json.Unmarshal(f, &database)
		unwrap(ok)
	} else if os.IsNotExist(err) {
		database.updateDatabase(c)

	} else {
		log.Fatal(err)
	}
	return database
}
func (d *Database) updateDatabase(c Config) {
	count := 0
	il := loadIgnoreList()
	vehiclePath := filepath.Join(c.BeamNGPath, "content", "vehicles/")
	levelPath := filepath.Join(c.BeamNGPath, "content", "levels/")
	smth := [2]string{vehiclePath, levelPath}
	var allModsPaths []string
	for _, set := range smth {
		files, err := os.ReadDir(set)
		unwrap(err)
		for _, file := range files {
			modPath := filepath.Join(set, file.Name())
			h, valid := createHash(modPath)
			if !valid {
				continue
			}
			existing, ok := d.Mods[h]
			if !ok {
				mod, isMod := readMod(modPath, il, &h)
				if isMod {
					d.Mods[mod.Hash] = mod
					allModsPaths = append(allModsPaths, mod.Path)
					count++
				}
			} else {
				if existing.Type == ModVehicle {
					existing.Enabled = !strings.HasSuffix(file.Name(), ".dis")
				}
				existing.Path = modPath
				existing.Name = strings.TrimSuffix(strings.TrimSuffix(file.Name(), ".dis"), ".zip")
				d.Mods[h] = existing
				allModsPaths = append(allModsPaths, existing.Path)
			}
		}
	}
	count = 0
	for _, mod := range d.Mods {
		if !slices.Contains(allModsPaths, mod.Path) {
			delete(d.Mods, mod.Hash)
			count++
		}
	}
	d.writeDatabase()
}

func createHash(filePath string) (uint64, bool) {
	if !strings.HasSuffix(filePath, ".zip") && !strings.HasSuffix(filePath, ".dis") {
		return 0, false
	}
	s, err := os.Stat(filePath)
	unwrap(err)
	if s.IsDir() {
		return 0, false
	}
	f, err := os.Open(filePath)
	unwrap(err)
	defer f.Close()
	h := fnv.New64a()
	_, err = io.Copy(h, f)
	unwrap(err)
	return h.Sum64(), true
}
func createSha(filePath string) string {
	f, err := os.Open(filePath)
	unwrap(err)
	defer f.Close()
	s := sha256.New()
	_, err = io.Copy(s, f)
	unwrap(err)
	sum := s.Sum(nil)
	return fmt.Sprintf("%x", sum)
}

func readMod(filePath string, il IgnoreList, h *uint64) (Mod, bool) {
	isMod := false
	var mod Mod
	if slices.Contains(il, filepath.Base(filePath)) {
		return mod, false
	}
	r, err := zip.OpenReader(filePath)
	if err == zip.ErrFormat {
		return mod, false
	} else {
		unwrap(err)
	}
	info, err := os.Stat(filePath)
	unwrap(err)
	mod.Size = int(info.Size())
	mod.Time = int(info.ModTime().Unix())
	mod.Name = strings.TrimSuffix(info.Name(), ".dis")
	mod.Name = strings.TrimSuffix(mod.Name, ".zip")
	defer r.Close()
	mod.Path = filePath
	if h == nil {
		fileHash, valid := createHash(filePath)
		if !valid {
			return mod, false
		}
		mod.Hash = fileHash
	} else {
		mod.Hash = *h
	}
	for _, f := range r.File {
		if strings.HasPrefix(f.Name, "levels") {
			mod.Type = ModMap
			mod.SHA = createSha(mod.Path)
			isMod = true
			break
		} else if strings.HasPrefix(f.Name, "vehicles") || strings.HasPrefix(f.Name, "mod_info") {
			if strings.HasSuffix(info.Name(), ".dis") {
				mod.Enabled = false
			} else {
				mod.Enabled = true
			}
			mod.Type = ModVehicle
			isMod = true
			break
		}
	}

	return mod, isMod
}

func getBeamNGPath() string {
	const beamngID = "284160"
	var steamRootPath string
	var libraryfolders map[string]any
	var beamngPath string
	steamRootPath = getSteamRoot()
	f, err := os.Open(filepath.Join(steamRootPath, "steamapps", "libraryfolders.vdf"))
	unwrap(err)
	defer f.Close()
	libraryfolders, err = vdf.NewParser(f).Parse()
	unwrap(err)
	var sas map[string]any = libraryfolders["libraryfolders"].(map[string]any)
	for _, v := range sas {
		var path string = v.(map[string]any)["path"].(string)
		for appID := range v.(map[string]any)["apps"].(map[string]any) {
			if appID == beamngID {
				beamngPath = filepath.Join(path, "steamapps", "common", "BeamNG.drive")
			}
		}

	}
	return beamngPath
}
func defaultConfig() Config {
	var config Config
	home, err := os.UserHomeDir()
	unwrap(err)
	config.DownloadsPath = filepath.Join(home, "Downloads", "Telegram Desktop")
	config.BeamNGPath = getBeamNGPath()
	config.SortType = Time
	switch runtime.GOOS {
	case "linux":
		config.BeamMpPath = filepath.Join(home, "Resources")
	case "windows":
		appdata, ok := os.LookupEnv("appdata")
		if !ok {
			log.Fatal("%appdata% not founded")
		}
		config.BeamMpPath = filepath.Join(appdata, "BeamMP-Launcher", "Resources")
	}
	return config
}

func getAppDirPath() string {
	var appDirPath string
	home, err := os.UserHomeDir()
	if err != nil {
		log.Fatal(err)
	}
	switch runtime.GOOS {
	case "linux":
		appDirPath = filepath.Join(home, ".local", "share", appName)
	case "windows":
		smth, ok := os.LookupEnv("LOCALAPPDATA")
		if !ok {
			log.Fatal("APPDATA was not found")
		}
		appDirPath = filepath.Join(smth, appName)
	default:
		log.Fatal("Unsupported OS")

	}
	return appDirPath
}
func getConfigPath() string {
	var configPath string
	configPath, err := os.UserConfigDir()
	if err != nil {
		log.Fatal(err)
	}
	return filepath.Join(configPath, appName+".json")
}

func (m *Mod) newMapPath(c Config) (string, bool) {
	if m.Type == ModMap {
		return filepath.Join(c.BeamMpPath, strings.TrimSuffix(m.Name, ".zip")+"-"+m.SHA[:8]+".zip"), true
	}
	return "", false
}

func getNewMods(c Config, d Database) []Mod {
	files, err := os.ReadDir(c.DownloadsPath)
	il := loadIgnoreList()
	var mods []Mod
	if err != nil {
		log.Fatal(err)
	}
	for _, file := range files {
		h, valid := createHash(filepath.Join(c.DownloadsPath, file.Name()))
		if !valid {
			continue
		}
		if _, ok := d.Mods[h]; !ok {
			mod, ok := readMod(filepath.Join(c.DownloadsPath, file.Name()), il, &h)
			if !ok {
				continue
			}
			mods = append(mods, mod)
		}
	}
	return mods
}
func copy(src, dst string) error {
	srcFileStat, err := os.Stat(src)
	unwrap(err)
	if !srcFileStat.Mode().IsRegular() {
		return fmt.Errorf("%s is not a regular file", src)
	}
	source, err := os.Open(src)
	unwrap(err)
	defer source.Close()

	dest, err := os.Create(dst)
	unwrap(err)
	defer dest.Close()
	_, err = io.Copy(dest, source)
	return err
}
func (d *Database) syncroniseDatabaseAndDownloads(c Config) {
	downloadedMods := getNewMods(c, *d)
	change := false
	levelsPath := getLevelsPath(c)
	vehiclesPath := getVehiclesPath(c)
	for _, mod := range downloadedMods {
		_, exists := d.Mods[mod.Hash]
		if !exists {
			mod.toggle(false)
			change = true
			var newPath string
			if _, ok := d.namesMods()[mod.Name]; ok {
				mod.Name += "_dup"
			}
			if mod.Type == ModMap {
				newPath = filepath.Join(levelsPath, mod.Name+".zip")
				shaPath, ok := mod.newMapPath(c)
				unwrap(ok)
				err := copy(mod.Path, shaPath)
				unwrap(err)
			} else {
				if mod.Enabled {
					newPath = filepath.Join(vehiclesPath, mod.Name+".zip")

				} else {
					newPath = filepath.Join(vehiclesPath, mod.Name+".zip.dis")
				}
			}
			err := os.Rename(mod.Path, newPath)
			unwrap(err)
			mod.Path = newPath
			d.Mods[mod.Hash] = mod
		}
	}
	if change {
		d.writeDatabase()
	}

}
func sortMods(a, b Mod, sortBy sortType) int {
	typeSort := sortBy
	if typeSort == "" {
		typeSort = Time
	}
	switch typeSort {
	case Time:
		if a.Time > b.Time {
			return -reverseSort
		} else if a.Time < b.Time {
			return reverseSort
		} else {
			return 0
		}
	case Size:
		if a.Size > b.Size {
			return -reverseSort
		} else if a.Size < b.Size {
			return reverseSort
		} else {
			return 0
		}
	case Name:
		return strings.Compare(a.Name, b.Name) * reverseSort
	default:
		fmt.Printf("Sorting type %s doesn't exist, check your spelling.\n", typeSort)
		os.Exit(1)
	}
	return 0
}
