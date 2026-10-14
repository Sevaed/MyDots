package main

import (
	"fmt"
	"hash/fnv"
	"io"
	"log"
	"os"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Not enough arguments")
		os.Exit(1)
	}
	file, err := os.Open(os.Args[1])
	if err != nil {
		panic(err)
	}
	defer file.Close()
	hash := fnv.New64a()
	if _, err := io.Copy(hash, file); err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%d %s", hash.Sum64(), os.Args[1])
}
