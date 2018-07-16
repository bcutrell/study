package main

import (
	"fmt"
	"math"
)

/*
Consider an analog clock face:
(1) Given a time of day as (hours, minutes),
write a funciton to calculate the angle between the hour and minute hand of the clock.
Assume that the minute hand only moves once per minute
*/

func minutesToDegrees(minutes float64) float64 {
	if minutes > 30 {
		minutes = 60 - minutes
	}

	return minutes * 6
}

func hoursToDegrees(hours float64, minutes float64) float64 {
	if hours > 6 {
		hours = 12 - hours
	}
	return (hours * 30) + minutes*0.5
}

func calculateAngle(hour float64, minutes float64) float64 {

	hour_degrees := hoursToDegrees(hour, minutes)
	minutes_degrees := minutesToDegrees(minutes)
	return math.Abs(hour_degrees - minutes_degrees)
}

func main() {

	result := calculateAngle(3.0, 15.0)
	if result == 7.5 {
		fmt.Println("Pass")
	} else {
		fmt.Println("Fail")
	}

}
