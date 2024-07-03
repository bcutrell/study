// Entertaining my 6 year old with chatGPT and a snake game
package main

import (
	"fmt"
	"math/rand"
	"time"

	"github.com/nsf/termbox-go"
)

const (
	width  = 40 // Width of the playing field
	height = 20 // Height of the playing field
)

type Point struct {
	x, y int
}

type Snake struct {
	body  []Point
	dir   Point
	alive bool
}

var snake Snake
var food Point

func main() {
	err := termbox.Init()
	if err != nil {
		panic(err)
	}
	defer termbox.Close()

	snake = Snake{
		body:  []Point{{x: width / 2, y: height / 2}},
		dir:   Point{0, 1},
		alive: true,
	}

	placeFood()

	go func() {
		for snake.alive {
			time.Sleep(200 * time.Millisecond)
			update()
			draw()
		}
	}()

	eventLoop()
}

func placeFood() {
	rand.Seed(time.Now().UnixNano())
	food = Point{rand.Intn(width-2) + 1, rand.Intn(height-2) + 1}
}

func update() {
	head := snake.body[0]
	newHead := Point{head.x + snake.dir.x, head.y + snake.dir.y}

	if newHead.x <= 0 || newHead.x >= width-1 || newHead.y <= 0 || newHead.y >= height-1 {
		snake.alive = false
		return
	}

	for _, p := range snake.body {
		if p == newHead {
			snake.alive = false
			return
		}
	}

	if newHead == food {
		snake.body = append([]Point{newHead}, snake.body...)
		placeFood()
	} else {
		snake.body = append([]Point{newHead}, snake.body[:len(snake.body)-1]...)
	}
}

func draw() {
	termbox.Clear(termbox.ColorDefault, termbox.ColorDefault)

	// Draw the border
	for x := 0; x < width; x++ {
		termbox.SetCell(x, 0, '#', termbox.ColorWhite, termbox.ColorDefault)
		termbox.SetCell(x, height-1, '#', termbox.ColorWhite, termbox.ColorDefault)
	}
	for y := 0; y < height; y++ {
		termbox.SetCell(0, y, '#', termbox.ColorWhite, termbox.ColorDefault)
		termbox.SetCell(width-1, y, '#', termbox.ColorWhite, termbox.ColorDefault)
	}

	// Draw the snake
	for _, p := range snake.body {
		termbox.SetCell(p.x, p.y, 'O', termbox.ColorGreen, termbox.ColorDefault)
	}

	// Draw the food
	termbox.SetCell(food.x, food.y, 'X', termbox.ColorRed, termbox.ColorDefault)
	termbox.Flush()
}

func eventLoop() {
	for snake.alive {
		switch ev := termbox.PollEvent(); ev.Type {
		case termbox.EventKey:
			switch ev.Key {
			case termbox.KeyArrowUp:
				if snake.dir.y != 1 {
					snake.dir = Point{0, -1}
				}
			case termbox.KeyArrowDown:
				if snake.dir.y != -1 {
					snake.dir = Point{0, 1}
				}
			case termbox.KeyArrowLeft:
				if snake.dir.x != 1 {
					snake.dir = Point{-1, 0}
				}
			case termbox.KeyArrowRight:
				if snake.dir.x != -1 {
					snake.dir = Point{1, 0}
				}
			case termbox.KeyEsc:
				snake.alive = false
			}
		case termbox.EventError:
			panic(ev.Err)
		}
	}

	fmt.Println("Game Over")
}
