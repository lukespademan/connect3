from microbit import *
import radio
import music

radio.config(channel=86)
radio.on()


def send_board(board):
    """send board to display and to other micro:bit"""
    radio.send(board)
    display.show(Image(board))


def get_board_pixel(x, y, board):
    pos = get_pos(x, y)
    value = board[pos]
    return value


def set_board_pixel(x, y, board, colour):
    pos = get_pos(x, y)
    board = board[:pos] + str(colour) + board[pos+1:]
    return board


def get_pos(x, y):
    pos = (6*y) + x
    return pos


def fall(x, y, board, colour):
    set_board_pixel(x, y, board, colour)
    send_board(board)
    falling = True
    while falling:
        if y >= 4 or get_board_pixel(x, y+1, board) != "0":  # if above another 'couner' or at bottom of LED matrix
            falling = False
        else:
            y += 1
            board = set_board_pixel(x, y, board, colour)  # moves counter down by one
            board = set_board_pixel(x, y-1, board, 0)  # removes counter from above
            send_board(board)
            sleep(500)  # waits for 0.5 seconds so animation can be seen
    return board


def congradulate():
    radio.send("IW")
    display.show(Image.HAPPY)
    music.play(music.BA_DING)
    exit()

def defeat():
    display.show(Image.SAD)
    music.play(music.DADADADUM)
    exit()

def detect_win(board):
    rows = board.split(":")
    won = False
    for row in rows:
        for i in range(3):
            colour = row[i]
            if colour != "0":
                if row[i] == row[i+1] == row[i+2]:
                    print(row)
                    return colour
    for col in range(3):
        for row in range(5):
            colour = rows[col][row]
            if colour != "0":
                if rows[col][row] == rows[col+1][row] == rows[col+2][row]:
                    print(colour)
                    return colour
    for col in range(3):
        for row in range(3):
            colour = rows[col][row]
            if colour != "0":
                if rows[col][row] == rows[col+1][row+1] == rows[col+2][row+2]:
                    return colour
    for col in range(4, 1, -1):
        for row in range(3):
            colour = rows[col][row]
            if colour != "0":
                print(col ,row)
                if rows[col][row] == rows[col - 1][row + 1] == rows[col - 2][row + 2]:
                    return colour
    return None


my_colour = "4"
my_turn = False
board = "00000:00000:00000:00000:00000"
x = 0
y = 0
while True:
    if my_turn:
        if button_a.is_pressed():
            x += 1
            while get_board_pixel(x, 1, board) != "0":
                x += 1
                if x > 5:
                    x = 0
            row = ["0", "0", "0", "0", "0"]
            row[x] = my_colour
            for c, pixel_colour in enumerate(row):
                board = set_board_pixel(c, 0, board, pixel_colour)
            send_board(board)
            sleep(250)
        if button_b.is_pressed():
            board = fall(x, y, board, my_colour)
            if detect_win(board):
                display.show(Image(my_colour*25))
                radio.send("IW")
                break
            else:
                my_turn = False
                radio.send("YT")
    else:
        data = radio.receive()
        if data:
            if data == "YT":
                my_turn = True
            elif data == "IW":
                defeat()
            else:
                board = data
                display.show(Image(data))
