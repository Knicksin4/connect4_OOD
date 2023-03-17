import enum

class GridPosition(enum.Enum):
    EMPTY = 0,
    YELLOW = 1,
    RED = 2

# Grid can have variable parameters so we will set that when we establish our grid
#otherwise e would have to hardcode the dimensions
class Grid:
    def __init__(self, rows, cols,):
        self._rows = rows
        self._cols = cols
        self._grid = None
        self.initGrid() # we can also pass the rows and cols into this method for a different approach

    def initGrid(self):
        self._grid = ([[GridPosition.EMPTY for _ in range(self._cols)]
                       for _ in range(self._rows)])
    def getGrid(self):
        return self._grid

    def getColCount(self):
        return self._cols

    def placePiece(self, col, piece):
        if col < 0 or col >= self._cols:
            raise ValueError('Invalid column')
        if piece == GridPosition.EMPTY:
            raise ValueError('Invalid piece')
        for row in range(self._rows-1, -1, -1):
            if self._grid[row][col] == GridPosition.EMPTY:
                self._grid[row][col] = piece
                return row

    def checkWin(self, connectN, row, col, piece):
        count = 0
        # check horizontal
        for c in range(self._cols):
            if self._grid[row][c] == piece:
                count += 1
            else:
                count = 0
            if count == connectN:
                return True
        #check vertical

        count = 0
        for r in range(self._rows):
            if self._grid[r][col] == piece:
                count += 1
            else:
                count = 0
            if count == connectN:
                return True
        # check diagonal
        count = 0
        for r in range(self._rows):
            c = row + col - r
            if c >= 0 and c < self._cols and self._grid[r][c] == piece:
                count += 1
            else:
                count = 0
            if count == connectN:
                return True

        # check diagonal
        count = 0
        for r in range(self._rows):
            c = col - row + r
            if c >= 0 and c < self._cols and self._grid[r][c] == piece:
                count += 1
            else:
                count = 0
            if count == connectN:
                return True
        return False

class Player:
    def __init__(self, name, pieceColor):
        self.name = name
        self.pieceColor = pieceColor

    def getName(self):
        return self.name

    def getPieceColor(self):
        return self.pieceColor

class Game:
    def __init__(self, grid, connectN, targetScore):
        self._grid = grid
        self._connectN = connectN
        self._targetScore = targetScore

        self._players = [
            Player('Player 1', GridPosition.YELLOW),
            Player('Player 2', GridPosition.RED)
        ]

        self._score = {}
        for player in self._players:
            self._score[player.getName()] = 0

    def printBoard(self):
        print('Board:\n')
        grid = self._grid.getGrid()
        for i in range(len(grid)):
            row = ''
            for piece in grid[i]:
                if piece == GridPosition.EMPTY:
                    row += '0 '
                elif piece == GridPosition.YELLOW:
                    row += 'Y '
                elif piece == GridPosition.RED:
                    row += 'R '
            print(row)
        print('')

    def playMove(self, player):
        self.printBoard()
        print(f"{player.getName()}'s turn")
        colcnt = self._grid.getColCount()
        movecol = int(input(f"Enter Column between {0} and {colcnt - 1} to add piece"))
        moverow = self._grid.placePiece(movecol, player.getPieceColor())
        return (moverow, movecol)

    def playRound(self):
        while True:
            for player in self._players:
                row,col = self.playMove(player)
                pieceColor = player.getPieceColor()
                if self._grid.checkWin(self._connectN, row, col, pieceColor):
                    self._score[player.getName()] += 1
                    return player

    def play(self):
        maxScore = 0
        winner = None
        while maxScore < self._targetScore:
            winner = self.playRound()
            print(f"{winner.getName()} won the round")
            maxScore = max(self._score[winner.getName()], maxScore)

            self._grid.initGrid() # resets grid

        print(f"{winner.getName()} won the game")

grid = Grid(8,8)
game = Game(grid, 4, 2)
game.play()
