package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
)

type LocationArea struct {
	Name string `json:"name"`
}

type LocationAreasResponse struct {
	Results []LocationArea `json:"results"`
}

func fetchLocationAreas() ([]LocationArea, error) {
	response, err := http.Get("https://pokeapi.co/api/v2/location-area?limit=20")
	if err != nil {
		return nil, err
	}
	defer response.Body.Close()

	body, err := ioutil.ReadAll(response.Body)
	if err != nil {
		return nil, err
	}

	var locationAreasResponse LocationAreasResponse
	err = json.Unmarshal(body, &locationAreasResponse)
	if err != nil {
		return nil, err
	}

	return locationAreasResponse.Results, nil
}

func main() {
	var input string
	fmt.Print("pokedex > ")
	fmt.Scanln(&input)

	if input == "help" {
		fmt.Println("This is a Pokedex CLI. You can use it to search for Pokemon, view their stats, and more.")
	} else if input == "exit" {
		fmt.Println("Exiting the program.")
		os.Exit(0)
	} else if input == "map" {
		locationAreas, err := fetchLocationAreas()
		if err != nil {
			fmt.Println("Error fetching location areas:", err)
			return
		}

		fmt.Println("First 20 Location Areas:")
		for _, area := range locationAreas {
			fmt.Println("-", area.Name)
		}
	} else {
		fmt.Println("Running main.go")
		fmt.Println("You entered:", input)
	}
}
