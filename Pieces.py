from PIL import Image, ImageTk

class Piece:
    def __init__(self, color: str) -> None:
        self.color = color
        self.imgId = None
        self.isMoved = False
    

    def checkRange(self, row, col):
        if row > 7 or row <0:
            return False
        if col > 7 or col <0:
            return False
        return True
    
    def checkFreeSpace(self, row, col, board: list[list]):
       if self.checkRange(row, col):
           if board[row][col] is None:
               return True
           if board[row][col].color != self.color:
               return True
           else:
               return False
       else:
           return False

    def validMoves(self, row: int, col: int, board: list[list]) -> list[(int, int)]:
        return []
    
    def pawnOnOppositeSide(self, isOver, board: list[list], callback):
        pass

    def makeMove(self, oldRow, oldCol, newRow, newCol, sqrSize, sqrX1, sqrY1, 
                 piecesTaken, board, canvas):
        piece: Piece = board[oldRow][oldCol]
        self.isMoved = True
        # take piece if its different color
        if board[newRow][newCol] is not None:
            piecesTaken[board[newRow][newCol].color].append(board[newRow][newCol])

        board[newRow][newCol] = board[oldRow][oldCol]
        board[oldRow][oldCol] = None
        canvas.coords(piece.imgId, sqrX1 + sqrSize//2, sqrY1 + sqrSize//2)

    def tkImage(self, size) -> ImageTk.PhotoImage:
        img = Image.open(self.path)
        img = img.resize((int(size), int(size)))
        return ImageTk.PhotoImage(img)

class Pawn(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        if color == "b":
            self.path = "./img/pawnB.png"
        else:
            self.path = "./img/pawnW.png"

    def pawnOnOppositeSide(self, isOver, board: list[list], callback):
        if isOver == False:
            if self.color == "w":
                if self in board[0]:
                    callback("w", 0, board[0].index(self))
            if self.color == "b":
                if self in board[-1]:
                    callback("b", -1, board[-1].index(self))
                   
    
    def validMoves(self, row: int, col: int, board: list[list]) -> list[(int, int)]:
        res = []
        if self.color == "b":
            if board[row + 1][col] is None:
                res.append((row + 1, col))
            if ((self.isMoved == False) and board[row + 1][col] is None and 
                board[row + 2][col] is None):
                res.append((row + 2, col))
                
            if (col + 1 < 8 and board[row+1][col+1] is not None and 
                board[row+1][col+1].color != "b"):
                res.append((row+1, col+1))
            if (col - 1 > -1 and board[row+1][col-1] is not None and 
                board[row+1][col-1].color != "b"):
                res.append((row+1, col-1))
                
        else:
            if board[row - 1][col] is None:
                res.append((row - 1, col))
            if ((not self.isMoved) and board[row - 1][col] is None and 
                board[row - 2][col] is None):
                res.append((row - 2, col))
            if (col + 1 < 8 and board[row - 1][col + 1] is not None and 
                board[row - 1][col + 1].color != "w"):
                res.append((row - 1, col + 1))
            if (col - 1 > -1 and board[row - 1][col - 1] is not None and 
                board[row - 1][col - 1].color != "w"):
                res.append((row-1, col-1))
        return res
        

class Rook(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        if color == "b":
            self.path = "./img/rookB.png"
        else:
            self.path = "./img/rookW.png"

    def validMoves(self, row: int, col: int, board: list[list]) -> list[(int, int)]:
         res = []
         moves = [(0,-1),(0,1),(1,0),(-1,0)]
         for mRow, mCol in moves:
             for i in range(1,8):
                 newRow = row + (i*mRow)
                 newCol = col + (i*mCol)
                 if self.checkFreeSpace(newRow, newCol, board):
                     res.append((newRow, newCol))
                     if (board[newRow][newCol] is not None and 
                         board[newRow][newCol].color != self.color):
                         break
                 else:
                     break
         return res


class Knight(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        if color == "b":
            self.path = "./img/knightB.png"
        else:
            self.path = "./img/knightW.png"
    
    def validMoves(self, row: int, col: int, board: list[list]) -> list[(int, int)]:
        res = []
        lMoves = [(-2,-1), (-2,1), (-1,-2), (-1,2), (2,-1), (2,1), (1,-2), (1,2)]
        for mRow, mCol in lMoves:
            if self.checkFreeSpace(row+mRow, col+mCol, board):
                res.append((row+mRow, col+mCol))
        return res

class Bishop(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        if color == "b":
            self.path = "./img/bishopB.png"
        else:
            self.path = "./img/bishopW.png"
    
    def validMoves(self, row: int, col: int, board: list[list]) -> list[(int, int)]:
        res = []
        moves = [(1,1),(1,-1),(-1,-1),(-1,1)]
        for mRow, mCol in moves:
            for i in range(1,8):
                newRow = row + (i * mRow)
                newCol = col + (i * mCol)
                if self.checkFreeSpace(newRow, newCol, board):
                    res.append((newRow, newCol))
                    if (board[newRow][newCol] is not None and 
                        board[newRow][newCol].color != self.color):
                        break
                else:
                    break
        return res
    

class Queen(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        if color == "b":
            self.path = "./img/queenB.png"
        else:
            self.path = "./img/queenW.png"

    def validMoves(self, row: int, col: int, board: list[list]) -> list[(int, int)]:
        res = []
        moves = [(0,-1),(0,1),(1,0),(-1,0), (1,1),(1,-1),(-1,-1),(-1,1)]
        for mRow, mCol in moves:
            for i in range(1,8):
                newRow = row + (i * mRow)
                newCol = col + (i * mCol)
                if self.checkFreeSpace(newRow, newCol, board):
                    res.append((newRow, newCol))
                    if (board[newRow][newCol] is not None and 
                        board[newRow][newCol].color != self.color):
                        break
                else:
                    break
        return res

class King(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        if color == "b":
            self.path = "./img/kingB.png"
        else:
            self.path = "./img/kingW.png"

    def validMoves(self, row: int, col: int, board: list[list]) -> list[(int, int)]:
        res = []
        moves = [(-1,0),(-1,1),(-1,-1),(0,-1),(0,1),(1,1),(1,0),(1,-1)]
        for mRow, mCol in moves:
            if self.checkFreeSpace(row + mRow, col + mCol, board):
                res.append((row + mRow, col + mCol))
        return res
