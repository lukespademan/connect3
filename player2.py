from microbit import *
import radio

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


def detect_win(board):
    rows = board.split(":")
    won = False
    """checks for 3 in a row"""
    for row in rows:
        c = ""
        for i in range(3):
            if row[i] != "0":
                c = row[i]
                if row[i] == row[i+1] == row[i+2]:
                    won = True
                    return won
    """checks for 3 in a col"""
    for row in range(3):
        c = ""
        for col in range(5):
            if rows[row][col] != "0":
                c = rows[row][col]
                if rows[row][col] == rows[row+1][col] == rows[row+2][col]:
                    won = True
                    return won
    """checks for 3 in a y=-x+c diag"""
    for row in range(3):
        c = ""
        for col in range(3):
            if rows[row][col] != "0":
                c = rows[row][col]
                if rows[row][col] == rows[row+1][col+1] == rows[row+2][col+2]:
                    won = True
                    return won
    """checks for 3 in a y=x+c diag"""
    rows = rows[::-1]
    for i in rows:
        rows[i] = rows[i][::-1]
    for row in range(3):
        c = ""
        for col in range(3):
            if rows[row][col] != "0":
                c = rows[row][col]
                if rows[row][col] == rows[row+1][col+1] == rows[row+2][col+2]:
                    won = True
                    return won

    return won


def main():
    board = "00000:" \
            "00000:" \
            "00000:" \
            "00000:" \
            "00000:"
    send_board(board)
    x = 4
    y = 0
    my_colour = "3"
    my_turn = False
    while True:
        if my_turn:
            if button_a.is_pressed():
                x += 1
                while get_board_pixel(x, 1, board) != "0":  # until there is no counter underneath
                    x += 1  # move along.
                    if x > 5:  # when your at the end go to the start
                        x = 0
                row = ["0", "0", "0", "0", "0"]
                row[x] = my_colour  # set the pixel at the top, where you are to your colour (brightness)
                for c, pixel_colour in enumerate(row):  # counter acts as x co-ord
                    board = set_board_pixel(c, 0, board, pixel_colour)  # update the pixels on the board
                send_board(board)
                sleep(250)  # allows recognition of one press
            if button_b.is_pressed():
                board = fall(x, y, board, my_colour)
                if won(board):
                    display.show(Image("my_colour"*25))
                    radio.send("IW")
                    break
                else:
                    my_turn = False
                    radio.send("YT")  # sends 'Your Turn' Message
        else:
            data = radio.receive()
            if data:
                if data == "YT":  # if they tell me its my turn
                    my_turn = True
                elif data == "IW":
                    display.scroll("Lost")
                else:
                    board = data
                    display.show(Image(data))


main()
