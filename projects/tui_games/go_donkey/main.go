package main

import (
	"fmt"
	"os"
	"os/exec"
	"time"

	"github.com/eiannone/keyboard"
)

const (
	WIDTH  = 40
	HEIGHT = 20
)

func handleInput(p *Player) {
	char, _, err := keyboard.GetKey()
	if err != nil {
		return
	}

	switch char {
	case 'a':
		p.x--
	case 'd':
		p.x++
	case ' ':
		if !p.jumping {
			p.jumping = true
			p.velY = -2.0
		}
	}
}

type Player struct {
	x, y    int
	sprite  rune
	jumping bool
	velY    float64
}

func NewPlayer() *Player {
	return &Player{
		x:      5,
		y:      HEIGHT - 5,
		sprite: '@',
	}
}

func (p *Player) update() {
	// Apply gravity
	if p.jumping {
		p.velY += 0.5 // gravity
		p.y += int(p.velY)

		// Hit ground
		if p.y >= HEIGHT-1 {
			p.y = HEIGHT - 1
			p.jumping = false
			p.velY = 0
		}
	}
}

type Platform struct {
	x, y, width int
}

func NewPlatform(x, y, width int) *Platform {
	return &Platform{
		x:     x,
		y:     y,
		width: width,
	}
}

func (p *Platform) collidesWith(player *Player) bool {
	return player.y == p.y &&
		player.x >= p.x &&
		player.x < p.x+p.width
}

type Game struct {
	screen    [][]rune
	player    *Player
	platforms []*Platform
}

func (g *Game) render() {
	cmd := exec.Command("clear")
	cmd.Stdout = os.Stdout
	cmd.Run()

	for _, row := range g.screen {
		fmt.Println(string(row))
	}
}
func NewGame() *Game {
	g := &Game{
		screen:    make([][]rune, HEIGHT),
		player:    NewPlayer(),
		platforms: make([]*Platform, 0),
	}

	// Add platforms
	g.platforms = append(g.platforms, NewPlatform(5, HEIGHT-3, 10))
	g.platforms = append(g.platforms, NewPlatform(20, HEIGHT-6, 8))

	for i := range g.screen {
		g.screen[i] = make([]rune, WIDTH)
	}
	return g
}

func (g *Game) update() {
	// Clear screen
	for i := range g.screen {
		for j := range g.screen[i] {
			g.screen[i][j] = ' '
		}
	}

	// Update player
	g.player.update()

	// Draw platforms
	for _, platform := range g.platforms {
		for i := 0; i < platform.width; i++ {
			g.screen[platform.y][platform.x+i] = '='
		}
	}

	// Draw player
	g.screen[g.player.y][g.player.x] = g.player.sprite
}

func main() {
	game := NewGame()
	keyboard.Open()
	defer keyboard.Close()

	for {
		handleInput(game.player)
		game.update()
		game.render()
		time.Sleep(50 * time.Millisecond)
	}
}
