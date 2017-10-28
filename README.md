# micro:bit connect3
Comments have been removed in some places due to the file size limit on the bbc micro:bits

## player1.py
This is the code for the first micro:bit. They get to go first.

## player2.py
This is the code for the second micro:bit.

## player0.py
Player 0 can be flashed to both micro:bits instead of player1.py and player2.py, and lets the micro:bits decide who is player1/player2. Allows Only 1 file needed, and no memory of which code is on which micro:bit, and I don't have to edit future code in 2 places. 

## viewer.py
This runs on a third micro:bit. It is optional to use. It acts like a second
monitor, just displaying the game board. It sends the data over serial to a
Rapberry Pi with a sense hat

## display.py
To be run on a raspberry pi with a sense hat. Gets data from a micro:bit over
serial, and displays it on and RGB LED matrix
