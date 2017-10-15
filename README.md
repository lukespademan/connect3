# micro:bit connect3
## player1.py
This is the code for the first micro:bit. They get to go first.

## player2.py
This is the code for the second micro:bit.

## viewer.py
This runs on a third micro:bit. It is optional to use. It acts like a second
monitor, just displaying the game board. It sends the data over serial to a
Rapberry Pi with a sense hat

## display.py
To be run on a raspberry pi with a sense hat. Gets data from a micro:bit over
serial, and displays it on and RGB LED matrix
