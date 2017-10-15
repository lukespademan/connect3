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
p1 = (0, 0, 255)
p2 = (255, 0, 0)
blank = (255, 255, 255)

while True:
    data = s.readline().decode("UTF-8").rstrip()
    formated = []

    count = 0
    for i in range(8*3):
        formated.append(blank)
    for c in data:
        if c != ":":
            if c == "5":
                formated.append(p2)
            if c == "9":
                formated.append(p1)
            if c == "0":
                formated.append(blank)
            if count == 4:
                formated.append(blank)
                formated.append(blank)
                formated.append(blank)
                count = -1
            count += 1
    
    sense.set_pixels(formated)

sense.clear()
s.close()
