package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

type LocationArea struct {
	Name string `json:"name"`
}

type LocationAreasResponse struct {
	Results  []LocationArea `json:"results"`
	Next     string         `json:"next"`
	Previous string         `json:"previous"`
}

func fetchLocationAreas(url string) (LocationAreasResponse, error) {
	if url == "" {
		url = "https://pokeapi.co/api/v2/location-area?limit=20"
	}

	fmt.Println("Fetching location areas from", url)
	response, err := http.Get(url)
	if err != nil {
		return LocationAreasResponse{}, err
	}
	defer response.Body.Close()

	body, err := io.ReadAll(response.Body)
	if err != nil {
		return LocationAreasResponse{}, err
	}

	var locationAreasResponse LocationAreasResponse
	err = json.Unmarshal(body, &locationAreasResponse)
	if err != nil {
		return LocationAreasResponse{}, err
	}

	return locationAreasResponse, nil
}

func main() {
	var input string
	var nextURL string
	var prevURL string

	// print instructions
	fmt.Println("Type 'help' for instructions, 'exit' to quit, or 'map' to view the first 20 location areas.")

	// prompt user for input
	for {
		fmt.Print("pokedex > ")
		fmt.Scanln(&input)

		if input == "help" {
			fmt.Println("This is a Pokedex CLI. You can use it to search for Pokemon, view their stats, and more.")
			fmt.Println("Commands:")
			fmt.Println("- help: view instructions")
			fmt.Println("- exit: quit the program")
			fmt.Println("- map: view the next 20 location areas")
			fmt.Println("- mapb: view the last 20 location areas (bonus)")
		} else if input == "exit" {
			fmt.Println("Exiting the program.")
			os.Exit(0)
		} else if input == "map" {
			response, err := fetchLocationAreas(nextURL)
			if err != nil {
				fmt.Println("Error fetching location areas:", err)
				return
			}
			locationAreas := response.Results
			nextURL = response.Next
			prevURL = response.Previous

			fmt.Println("Next 20 Location Areas:")
			for _, area := range locationAreas {
				fmt.Println("-", area.Name)
			}
		} else if input == "mapb" {
			if prevURL == "" {
				fmt.Println("No previous location areas to display.")
				continue
			}

			response, err := fetchLocationAreas(prevURL)
			if err != nil {
				fmt.Println("Error fetching location areas:", err)
				return
			}
			locationAreas := response.Results
			nextURL = response.Next
			prevURL = response.Previous

			fmt.Println("Last 20 Location Areas:")
			for _, area := range locationAreas {
				fmt.Println("-", area.Name)
			}
		} else {
			fmt.Printf("Invalid command %s. Type 'help' for instructions.\n", input)
		}
	}
}
