# connected to raspberry pi
from microbit import *
import radio

radio.config(channel=86)
radio.on()


while True:
    data = radio.receive()
    if data:
        if not(data in ("YT", "IW")):
            display.show(Image(data))
            print(data)
