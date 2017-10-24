import serial
from time import sleep
from sense_hat import SenseHat

sense = SenseHat()

PORT = "/dev/ttyACM0"
BAUD = 115200

s = serial.Serial(PORT)
s.baudrate = BAUD
s.parity = serial.PARITY_NONE
s.databits = serial.EIGHTBITS
s.stopbits = serial.STOPBITS_ONE
sense.show_letter("~")
sleep(0.5)
player1 = (0, 0, 255)
player2 = (255, 0, 0)
blank = (0, 0, 0)
edge = (100, 100, 100)

while True:
    data = s.readline().decode("UTF-8").rstrip()
    data_s = data.split(":")

    formatted = []  # will store data to send to LED matrix

    for i in range(8*2):  # top two rows
        formatted.append(edge)

    for row in data_s:
        formatted.append(edge)  # first col is an edge
        for c in row:
            if c == "4":
                formatted.append(player2)
            if c == "9":
                formatted.append(player1)
            if c == "0":
                formated.append(blank)
        formatted.append(edge)  # two thick edge on right side
        formatted.append(edge)

    for i in range(8):
        formatted.append(edge)
    sense.set_pixels(formated)
