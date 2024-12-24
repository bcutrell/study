package main

import (
	"fmt"
	"golang.org/x/term"
	"os"
	"os/exec"
	"time"
)

const (
	width        = 40
	height       = 8
	playerChar   = "@"
	obstacleChar = "#"
)

type Position struct {
	x int
	y int
}

type Game struct {
	playerPos  Position
	obstacles  []Position
	score      int
	isGameOver bool
}

func clearScreen() {
	cmd := exec.Command("clear") // Use "cls" for Windows
	cmd.Stdout = os.Stdout
	cmd.Run()
}

func (g *Game) draw() {
	clearScreen()

	// Draw score
	fmt.Printf("Score: %d\n", g.score)

	// Draw game area
	for h := 0; h < height; h++ {
		for w := 0; w < width; w++ {
			if h == g.playerPos.y && w == g.playerPos.x {
				fmt.Print(playerChar)
			} else if g.hasObstacle(w, h) {
				fmt.Print(obstacleChar)
			} else {
				fmt.Print(" ")
			}
		}
		fmt.Println()
	}
}

func (g *Game) hasObstacle(x, y int) bool {
	for _, obs := range g.obstacles {
		if obs.x == x && obs.y == y {
			return true
		}
	}
	return false
}

func (g *Game) update() {
	// Move obstacles left
	newObstacles := []Position{}
	for _, obs := range g.obstacles {
		obs.x--
		if obs.x >= 0 {
			newObstacles = append(newObstacles, obs)
		}
	}
	g.obstacles = newObstacles
	g.score += len(g.obstacles) - len(newObstacles)

	// Add new obstacle
	if len(g.obstacles) < 5 && time.Now().UnixNano()%7 == 0 {
		// Random y position for obstacle
		y := int(time.Now().UnixNano()%int64(height-2)) + 1
		g.obstacles = append(g.obstacles, Position{width - 1, y})
	}

	// Check collision
	if g.hasObstacle(g.playerPos.x, g.playerPos.y) {
		g.isGameOver = true
	}
}

func main() {
	game := &Game{
		playerPos:  Position{5, height / 2},
		obstacles:  []Position{},
		score:      0,
		isGameOver: false,
	}

	// Save current terminal state
	oldState, err := term.MakeRaw(int(os.Stdin.Fd()))
	if err != nil {
		panic(err)
	}
	defer term.Restore(int(os.Stdin.Fd()), oldState)

	// Input handling goroutine
	go func() {
		var b []byte = make([]byte, 1)
		for {
			os.Stdin.Read(b)
			switch string(b) {
			case "a":
				if game.playerPos.x > 0 {
					game.playerPos.x--
				}
			case "d":
				if game.playerPos.x < width-1 {
					game.playerPos.x++
				}
			case "w":
				if game.playerPos.y > 0 {
					game.playerPos.y--
				}
			case "s":
				if game.playerPos.y < height-1 {
					game.playerPos.y++
				}
			case "q":
				game.isGameOver = true
				return
			}
		}
	}()

	// Main game loop
	for !game.isGameOver {
		game.draw()
		game.update()
		time.Sleep(100 * time.Millisecond)
	}

	clearScreen()
	fmt.Printf("\nGame Over! Final score: %d\n", game.score)
}
