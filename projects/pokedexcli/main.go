package main

import (
	"fmt"
	"os"
)

func main() {
	var input string
	fmt.Print("pokedex > ")
	fmt.Scanln(&input)

	if input == "help" {
		fmt.Println("This is a Pokedex CLI. You can use it to search for Pokemon, view their stats, and more.")
	} else if input == "exit" {
		fmt.Println("Exiting the program.")
		os.Exit(0)
	} else {
		fmt.Println("Running main.go")
		fmt.Println("You entered:", input)
	}
}
