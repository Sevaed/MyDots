package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"os"
	"strings"
	"time"
)

func unwrap(err any) {
	if err == nil {
		return
	}
	switch err.(type) {
	case error:
		log.Fatal(err)
	case bool:
		if !err.(bool) {
			os.Exit(1)
		}
	case string:
		log.Fatal(err)
	default:
		log.Fatal("Wrong usage of unwrap()")
	}
}

type Stager struct {
	Indent int
	Stage  int
	Start  time.Time
}

func (s *Stager) Open(name string) {
	fmt.Printf("\nStage %v: ", s.Stage)
	fmt.Println(name + ".\n{")
	s.Indent++
	s.Start = time.Now()
}
func (s *Stager) PrintIndent() {
	fmt.Print(strings.Repeat("    ", s.Indent))
}
func (s *Stager) Println(v ...any) {
	s.PrintIndent()
	fmt.Println(v...)
}
func (s *Stager) Printf(format string, v ...any) {
	s.PrintIndent()
	fmt.Printf(format, v...)
}
func (s *Stager) Close() {
	sas := time.Since(s.Start)
	if sas > time.Millisecond {
		fmt.Printf("}\nStage ended in %v.\n", sas)
	} else {
		fmt.Println("}\nStage ended really fast.")
	}
	s.Indent--
	s.Stage++

}

func askBool(q string) bool {
	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Printf("%s [Y/n]: ", q)
		ans, err := reader.ReadString('\n')
		if err != nil && err != io.EOF {
			return false
		}
		ans = strings.ToLower(strings.TrimSpace(ans))
		if err == io.EOF {
			return false
		}
		switch ans {
		case "", "y", "yes":
			return true
		case "n", "no":
			return false
		}
	}
}
