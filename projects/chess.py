import os

class Square:
    def __init__(self, row, col):
        self.piece = None
        self.color = 'black' if (row + col) % 2 else 'white'

class Board:
    def __init__(self):
        # create a 8x8 grid of squares
        self.grid = [[Square(i, j) for j in range(8)] for i in range(8)]

    def draw(self):
        # print a horizontal bar at the top of the board
        print('-' * 33)

        # loop through each row and column of the board
        for i, row in enumerate(self.grid):
            # print a vertical bar at the beginning of the row
            print('|', end=' ')

            for j, square in enumerate(row):
                # get the symbol for the piece on the square, or a space if the square is empty
                piece = square.piece
                symbol = piece.symbol if piece else ' '

                # color the square black or white based on its color attribute
                if square.color == 'black':
                    print(f'\033[40m{symbol}\033[0m', end=' ')
                else:
                    print(f'\033[47m{symbol}\033[0m', end=' ')

                # print a vertical bar after each square, except the last one
                if j < 7:
                    print('|', end=' ')

            # print a vertical bar at the end of the row
            print('|')

            # print a horizontal bar after each row, except the last one
            if i < 7:
                print('-' * 33)
            else:
                # print a horizontal bar at the bottom of the board
                print('-' * 33)



    def move_piece(self, start, end):
        # move a piece from the start square to the end square
        self.grid[start[0]][start[1]].piece = None
        self.grid[end[0]][end[1]].piece = piece

        # redraw the board
        self.draw()

    def check_game_over(self):
        # check if the game is over (e.g. checkmate or stalemate)
        pass

class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.has_moved = False

    def move(self, new_position):
        # move the piece to a new position on the board
        pass

    def get_possible_moves(self):
        # return a list of all possible positions that the piece can move to
        pass

class Player:
    def __init__(self, color):
        self.color = color

    def get_move(self):
        # prompt the player for their next move and return it
        start = input('Enter the coordinates of the piece you want to move (e.g. a1): ')
        end = input('Enter the coordinates of the square you want to move to (e.g. a2): ')

        # convert the input strings to positions on the board
        start = self.parse_input(start)
        end = self.parse_input(end)

        return start, end

    def parse_input(self, input_str):
        # convert the input string (e.g. 'a1') to a position on the board (e.g. (0, 0))
        col = ord(input_str[0]) - ord('a')
        row = int(input_str[1]) - 1
        return row, col

def clear_terminal():
    # clear the terminal using the 'clear' command
    os.system('clear')

def draw_board():
    # redraw the board
    board.draw()


if __name__ == '__main__':
    # create a new board and player
    board = Board()

    # create a new player
    player = Player('white')

    # start the game loop
    while True:
        # clear the terminal and redraw the board
        clear_terminal()
        draw_board()

        # get the player's move and make it
        move = player.get_move()
        board.move_piece(*move)
