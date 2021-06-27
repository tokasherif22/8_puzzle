from copy import deepcopy

import os
os.system("color")

COLOR = {
    "ANSI_RESET": "\u001B[0m",
    "ANSI_RED": "\u001B[31m",
    "ANSI_GREEN": "\u001B[32m"
}

# used for changing the text color
# https://bluesock.org/~willkg/dev/ansi.html
ANSI_RESET = "\u001B[0m"
ANSI_RED = "\u001B[31m"
ANSI_GREEN = "\u001B[32m"


class puzzleBoard():

    def __init__(self, initialState=[], cost=0, parent=None, randomize=False, randomSize=3):

        if randomize or not initialState:
            print("Generating Random Initial State")
            initialState = self.randomize(randomSize)

        # To make sure you entered a Squared Number for the board size
        self.checkSize(len(initialState), int(len(initialState)**0.5))

        # Initialize the board tiles
        self.tiles = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(initialState[self.size*i + j])
                if row[-1] == 0:
                    self.emptyTile = [i, j]
            self.tiles.append(row)

        # initialize the rest of the parameters
        self.cost = cost
        self.parent = parent

    # Used in the heap sort for comparisons
    def __lt__(self, state):
        return state.cost > self.cost

    # Method to make sure you enterd a squared number for the board size
    def checkSize(self, length, size):
        # board too small to be playable
        # in case you want to play with this board size
        # remove this condition and change the (elif size**2 == length) condition
        # to (if size**2 == length or length == 2)
        if size < 2:
            raise Exception(
                f"{ANSI_RED}INPUT SIZE IS TOO SMALL, MINIMUM SIZE IS 4{ANSI_RESET}")
        elif size**2 == length:
            self.size = size
            self.direction = "Input"
        else:
            raise Exception(
                f"{ANSI_RED}INCORRECT INPUT SIZE, YOUR INPUT {length} : CLOSEST SQUARE NUMBERS {size**2} OR {(size+1)**2}!!!{ANSI_RESET}")

    def displayBoard(self):
        for i in range(self.size):
            print([self.tiles[i][j] for j in range(self.size)])

    def displayBoard2(self):
        #    print("." + f"____"*self.size)
        for i in range(self.size):
            row = ""
            for j in range(self.size):
                #  if self.tiles[i][j] == 0:
                    row += f" {self.tiles[i][j]:02d}"
                    #   else:
            #      row += f"| {self.tiles[i][j]:02d}"
            print(row)
            #   print(f"|___"*self.size + f"|")

    def displayBoard3(self):
        #  print("****"*self.size)
        for i in range(self.size):
            row = ""
            for j in range(self.size):
                row += f"{ANSI_GREEN} {self.tiles[i][j]:02d}"
            print(row+f"{ANSI_RESET}")

    # return a new board state where the empty tile and the tile above it are swapped
    def moveUp(self):
        if self.emptyTile[0] != 0:
            self.moveTile([-1, 0])
            self.direction = "Move Up"
            return self

    # return a new board state where the empty tile and the tile below it are swapped
    def moveDown(self):
        if self.emptyTile[0] != self.size - 1:
            self.moveTile([1, 0])
            self.direction = "Move Down"
            return self

    # return a new board state where the empty tile and the tile left to it are swapped
    def moveLeft(self):
        if self.emptyTile[1] != 0:
            self.moveTile([0, -1])
            self.direction = "Move Left"
            return self

    # return a new board state where the empty tile and the tile right to it are swapped
    def moveRight(self):
        if self.emptyTile[1] != self.size - 1:
            self.moveTile([0, 1])
            self.direction = "Move Right"
            return self

    # do the swapping process
    def moveTile(self, tile):
        row = self.emptyTile[0] + (1 * tile[0])
        col = self.emptyTile[1] + (1 * tile[1])
        self.tiles[row][col], self.tiles[self.emptyTile[0]][self.emptyTile[1]] \
            = self.tiles[self.emptyTile[0]][self.emptyTile[1]], self.tiles[row][col]
        self.emptyTile = [row, col]

    # create a new instance of the puzzleBoard
    # otherwise Python will just use the same pointer over the copies
    def copy(self):
        return deepcopy(puzzleBoard(self.tilesToList(), parent=self, cost=self.cost+1))
    __copy__ = copy

    # change the 2-D matrix into 1-D list for ease of processing
    def tilesToList(self):
        return [tile for row in self.tiles for tile in row]

    # get a list of all the children nodes states of the current parent state
    def children(self):
        states = [self.copy() for i in range(4)]
        states[0].moveUp()
        states[1].moveDown()
        states[2].moveLeft()
        states[3].moveRight()
        return [states[i] for i in range(4) if states[i].emptyTile != self.emptyTile]

    # check if the initialState of the board can be solved or not
    def canBeSolved(self):
        if self.isSolved():
            return

        inv_count = 0
        for i in range(self.size-1):
            j = i + 1
            while j < self.size:
                print(self.tiles[j][i], self.tiles[i][j])
                if self.tiles[j][i] > 0 and self.tiles[j][i] > self.tiles[i][j]:
                    inv_count += 1
                j += 1
        print("el inv count "+inv_count)
        if inv_count % 2 != 0:
            raise Exception(
                f"{ANSI_RED}**PUZZLE CANNOT BE SOLVED**{ANSI_RESET}")

    # create a random board state
    def randomize(self, size=3):
        import random
        size = size ** 2
        return random.sample(range(size), size)

    def solution(self):
        return [i for i in range(self.size**2)]

    def isSolved(self):
        return self.tilesToList() == self.solution()
