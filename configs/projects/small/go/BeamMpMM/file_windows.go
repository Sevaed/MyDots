package main

import (
	"golang.org/x/sys/windows/registry"
)

func getSteamRootWindows() string {
	k, err := registry.OpenKey(registry.LOCAL_MACHINE, `SOFTWARE\Wow6432Node\Valve\Steam`, registry.QUERY_VALUE)
	unwrap(err)
	defer k.Close()
	S, _, err := k.GetStringValue("installPath")
	unwrap(err)
	return S

}
