
import random
import re

#let's create a board object to represent the minesweeper game 
#this is so we can just say "create new board object", or
#"dig here", or "render this game for this object"
class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        #Let's create the board

        #helper function 
        self.board = self.make_new_board() #plant the bombs
        self.assign_values_to_board()
        #initialize a set to keep track of locations we've uncovered
        #we'll save (row, col) tuples into the set
        self.dug = set()    #if we dig at 0, 0  the self.dug = {(0,0)}

    def make_new_board(self):
        #construct a board based on number of bombs and dimension size
        #we should construct a list of lists here, or whatever representation that you prefer
        #but since we have a 2D board, list of lists is more natural

        board =[[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        #plant the bombs 
        bombs_planted=0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 -1)
            row = loc//self.dim_size
            col = loc%self.dim_size

            if board[row][col] == '*':  #if there is already a bomb planted we are not going to increase the bombs planted instead we are going to keep gpong
                continue    #goes to next iteration, skips following code

            board[row][col]='*' #plants a bomb
            bombs_planted += 1

        return board
    
    def assign_values_to_board(self):
        #now that bombs are planted let's assign values (0-8) for all empty squares
        #representeing neighbouing bombs precomputed
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)


    def get_num_neighboring_bombs(self, row, col):
        #let's iterate through the neighbourign positions and sum up the number of bombs
        #top left:(row-1, col-1)
        #top middle:(row-1, col)
        #top right:(row-1, col+1)
        #left: (row, row-1)
        #right: (row, row+1)
        #bottom left:(row +1, col-1)
        #bottom middle: (row+1, col)
        #bottom right: (row+1, col+1)

        #make sure we dont go out of bounds

        num_neighboring_bombs=0
        #min and max are used to keep everything within bounds, if it is trying to reach -1, then the max is chosen between the 2(0), same for min(the min is chosen betewwen the dimension sizre and the rrow we are in)
        for r in range (max (0, row-1), min(self.dim_size-1 ,(row +1) ) + 1 ):
            for c in range (max(0, col-1), min(self.dim_size-1, (col+1)) + 1):
                if r==row and c==col:
                    continue    #original location of bomb, don't check 
                if self.board[r][c] == '*':
                    num_neighboring_bombs+=1
        return num_neighboring_bombs

    def dig(self, row, col):
        #dig at location, return true if dig is succesful, false if we dig into bomb
        #a few scenarios:
        #we dig a bomb, then we lose
        #dig where there are neighbouring bobms
        #dig where there are no bombs -> recursilvely dig neighbours
        self.dug.add((row, col))#keep track of where we have dug
        if self.board[row][col]=='*':
            return False
        elif self.board[row][col]>0:
            return True
        #if it's not  * or a number >0, then it is 0, this is what happens when it is 0:
        for r in range (max (0, row-1), min(self.dim_size-1 ,(row +1) ) + 1 ):
            for c in range (max(0, col-1), min(self.dim_size-1, (col+1)) + 1):
                if (r, c) in self.dug:#you've already dug here
                    continue
                self.dig(r,c)
        #if our initial dig didn't hit a bomb, we *shouldn't * hit a bomb here
        return True
        
    def __str__(self):
        #if you call print, it will print what this function returns, returns a string of boards to show player

        #we make a new array that represents what the user should see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col]=str(self.board[row][col])
                else:
                    visible_board[row][col]= ' '
        #put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

#play the game
def play(dim_size=10, num_bombs=10):
    #Step 1: Create the board and plant the bombs
    board = Board(dim_size, num_bombs)
    #Step 2: Show user board and ask where thet want to dig
    #Step 3a: if location is a bomb show game over message
    #Step 3b: if location is not a bomb, dig recursevley until each square is at leaset next to a bomb
    #Step 4: repeat steps 2 and 3a/b until there are no more places to dig, Victory!
    safe = True
    while len(board.dug)< board.dim_size ** 2 - num_bombs:
        print(board)
        user_input= re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))#0,3, this can handle spaces and commas, so 0,0 or 0, 0 or 0,   0
        row, col = int(user_input[0]), int(user_input[-1])  #takes first and last item, since the user_input is an array with fluff in the middle
        if row <0 or row >= board.dim_size or col <0 or col >= dim_size:
            print("Invalid location try again.")
            continue
        #if it's valid we dig
        safe = board.dig(row, col)
        if not safe:
            #this means that we have dug a bomb
            break   #game over
    
    if safe:
        print("CONGRATS! You are victoriuos")
    else:
        print("Sorry game over ")
        #let's reveal the whole board
        board.dug = [(r, c) for r in range (board.dim_size) for c in range (board.dim_size)]
        print(board)
if __name__ == '__main__':
    play()