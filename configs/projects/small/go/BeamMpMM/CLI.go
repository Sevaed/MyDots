package main

import (
	"context"
	"fmt"
	"github.com/urfave/cli/v3"
)

type asciiCode string

const (
	Reset  asciiCode = "\033[0m"
	Bold   asciiCode = "\033[1m"
	Dim    asciiCode = "\033[2m"
	Cyan   asciiCode = "\033[36m"
	Yellow asciiCode = "\033[33m"
	Green  asciiCode = "\033[32m"
	Red    asciiCode = "\033[1;31m"
)

func list(d Database, c Config) {
	mods := d.listMods(c.SortType)
	fmt.Printf("%s▼ Maps%s\n", Cyan, Reset)
	for i, mod := range mods[ModMap] {
		var prefix string
		if i != len(mods[ModMap])-1 {
			prefix = "├── "
		} else {
			prefix = "└── "
		}
		fmt.Printf("%s%s%s%s\n", Green, prefix, mod.Name, Reset)
	}
	fmt.Printf("%s▼ Vehicles%s\n", Cyan, Reset)
	for i, mod := range mods[ModVehicle] {
		var prefix string
		var postfix string
		var color asciiCode
		if i != len(mods[ModVehicle])-1 {
			prefix = "├── "
		} else {
			prefix = "└── "
		}
		if mod.Enabled {
			color = Green
			postfix = fmt.Sprintf("%s✓%s", Cyan, Reset)
		} else {
			color = Red
			postfix = fmt.Sprintf("%s×%s", Red, Reset)
		}
		fmt.Printf("%s%s%s %s\n", color, prefix, mod.Name, postfix)
	}
}

func toggle(d *Database, name ...string) {
	namesMods := d.namesMods()
	for _, modName := range name {
		for _, mod := range namesMods[modName] {
			mod.toggle()
			d.Mods[mod.Hash] = mod
		}
	}
	d.writeDatabase()
	fmt.Printf("Mods were toggled, database updated.\n")

}
func enable(d *Database, name ...string) {
	namesMods := d.namesMods()
	for _, modName := range name {
		for _, mod := range namesMods[modName] {
			mod.toggle(true)
			d.Mods[mod.Hash] = mod
		}
	}
	d.writeDatabase()
	fmt.Printf("Mods were enabled, database updated.\n")

}
func disable(d *Database, name ...string) {
	namesMods := d.namesMods()
	for _, modName := range name {
		for _, mod := range namesMods[modName] {
			mod.toggle(false)
			d.Mods[mod.Hash] = mod
		}
	}
	d.writeDatabase()
	fmt.Printf("Mods were disabled, database updated.\n")

}

func printModPacks(d Database) {
	modpacks := listModPacks()
	for _, modpack := range modpacks {
		fmt.Printf("Modpack %s, has %d out of %d mods enabled.\n", modpack.Name, len(modpack.EnabledMods), len(d.listMods("")[ModVehicle]))
	}
}
func loadModpackByName(mpn string, d *Database) error {
	if mpn == "" {
		return fmt.Errorf("NoNameProvided")
	}
	mpm := make(map[string]ModPack)
	for _, modPack := range listModPacks() {
		mpm[modPack.Name] = modPack
	}
	mp, ok := mpm[mpn]
	if ok {
		mp.loadModPack(d)
		fmt.Printf("Modpack %s was loaded.\n", mp.Name)
		return nil
	} else {
		fmt.Printf("Modpack %s wasn't found.\n", mpn)
		return fmt.Errorf("WasntFound")
	}
}
func updateModPack(name string, d Database) error {
	if name == "" {
		return fmt.Errorf("NoNameProvided")
	}
	mp, ok := mapModPacks()[name]
	if ok {
		mp.update(d)
		fmt.Printf("Modpack %s was updated from current database, %d mods enabled.\n", mp.Name, len(mp.EnabledMods))
	} else {
		mp = d.createModPack(name)
		fmt.Printf("Modpack %s was created with %d mods enabled, from current database.\n", mp.Name, len(mp.EnabledMods))
	}
	return nil
}
func removeModPack(name string) error {
	if name == "" {
		return fmt.Errorf("NoNameProvided")
	}
	mp, ok := mapModPacks()[name]
	if ok {
		ans := askBool(fmt.Sprintf("Modpack %s has %d mods enabled, remove it?\n", mp.Name, len(mp.EnabledMods)))
		if !ans {
			return nil
		}
		unwrap(mp.delete())
		fmt.Printf("Modpack %s was removed.\n", name)
		return nil
	} else {
		fmt.Printf("Modpack with name %s was not found.\n", name)
		return fmt.Errorf("WasntFound")
	}
}
func synchronize(d Database, c Config) {
	fmt.Println("Synchronization started, it will take some time.")
	d.syncroniseDatabaseAndDownloads(c)
	fmt.Printf("Database was syncronised with the downloads.\n")
}
func CLIinit(d *Database, cfg Config) *cli.Command {
	cmd := &cli.Command{
		Name:                  appName,
		Version:               "development",
		Usage:                 "Mod Manager for BeamMp",
		EnableShellCompletion: true,
		Commands: []*cli.Command{
			{
				Name:    "list",
				Aliases: []string{"l"},
				Usage:   "list all mods",
				Action: func(ctx context.Context, c *cli.Command) error {
					list(*d, cfg)
					return nil
				}},
			{
				Name:    "modpack",
				Aliases: []string{"mp"},
				Usage:   "manage modpacks",
				Commands: []*cli.Command{
					{
						Name:    "list",
						Aliases: []string{"lm"},
						Usage:   "list all modpacks",
						Action: func(ctx context.Context, c *cli.Command) error {
							printModPacks(*d)
							return nil
						},
					}, {
						Name:    "update",
						Aliases: []string{"u"},
						Usage:   "update modpack from current database state by name",
						Action: func(ctx context.Context, c *cli.Command) error {
							return updateModPack(c.Args().First(), *d)
						},
					},
					{
						Name:    "load",
						Aliases: []string{"l"},
						Usage:   "load modpack by name",
						Action: func(ctx context.Context, c *cli.Command) error {
							return loadModpackByName(c.Args().First(), d)
						},
					},
					{
						Name:    "remove",
						Aliases: []string{"e"},
						Usage:   "remove modpack by name",
						Action: func(ctx context.Context, c *cli.Command) error {
							return removeModPack(c.Args().First())
						},
					},
				},
			},
			{
				Name:    "mod",
				Aliases: []string{"m"},
				Usage:   "manage mods",
				Commands: []*cli.Command{
					{
						Name:    "toggle",
						Aliases: []string{"t"},
						Usage:   "toggle mods state",
						Action: func(ctx context.Context, c *cli.Command) error {
							toggle(d, c.Args().Slice()...)
							return nil
						},
					},
					{
						Name:    "enable",
						Aliases: []string{"e"},
						Usage:   "enables mods",
						Action: func(ctx context.Context, c *cli.Command) error {
							enable(d, c.Args().Slice()...)
							return nil
						},
					},
					{
						Name:    "disable",
						Aliases: []string{"d"},
						Usage:   "disables mods",
						Action: func(ctx context.Context, c *cli.Command) error {
							disable(d, c.Args().Slice()...)
							return nil
						},
					},
				},
			},
			{
				Name:    "synchronize",
				Aliases: []string{"sync", "s"},
				Usage:   "synchronize database with downloads",
				Action: func(ctx context.Context, c *cli.Command) error {
					synchronize(*d, cfg)
					return nil
				},
			},
		}}
	return cmd
}
