package main

import (
	"fmt"
	rg "github.com/gen2brain/raylib-go/raygui"
	rl "github.com/gen2brain/raylib-go/raylib"
)

func GUI() {
	rl.SetTraceLogLevel(rl.LogWarning)
	rl.SetConfigFlags(rl.FlagVsyncHint | rl.FlagWindowHighdpi | rl.FlagWindowResizable | rl.FlagWindowAlwaysRun)
	rl.InitWindow(800, 450, "Hello GUI")
	rl.SetTargetFPS(60)
	showMessageBox := false
	rg.LoadStyle("./style.rgs")
	rg.SetFont(rl.LoadFont("./font/Gilroy-Regular_0.ttf"))
	rg.SetStyle(rg.DEFAULT, rg.TEXT_SIZE, 13)
	rg.SetStyle(rg.DEFAULT, rg.TEXT_SPACING, 1)

	fmt.Println("Background:", rg.GetStyle(rg.DEFAULT, rg.BACKGROUND_COLOR))
	fmt.Println("Text size:", rg.GetStyle(rg.DEFAULT, rg.TEXT_SIZE))
	fmt.Println("Border width:", rg.GetStyle(rg.BUTTON, rg.BORDER_WIDTH))
	for !rl.WindowShouldClose() {
		rl.BeginDrawing()
		rl.ClearBackground(rl.GetColor(uint(rg.GetStyle(rg.DEFAULT, rg.BACKGROUND_COLOR))))

		if rg.Button(rl.Rectangle{X: 24, Y: 24, Width: 120, Height: 30}, "#191#Show Message") {
			showMessageBox = true
		}
		if showMessageBox {
			btnActive := rg.MessageBox(rl.Rectangle{X: 85, Y: 70, Width: 250, Height: 100}, "#191#Message box", "Hi! This is a message!", "Nice;Cool")
			if btnActive >= 0 {
				showMessageBox = false
			}
		}
		rl.EndDrawing()
	}
	rl.CloseWindow()
}
