package main

import (
	"os"
	"path/filepath"
)

func getSteamRoot() string {
	home, err := os.UserHomeDir()
	unwrap(err)
	return filepath.Join(home, ".steam", "steam")
}
