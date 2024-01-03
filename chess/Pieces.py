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
           if board[row][col] == None:
               return True
           if board[row][col].color != self.color:
               # self.piecesTaken[f"{board[row][col].color}"].append(board[row][col])
               #print(self.piecesTaken)
               return True
           else:
               return False
       else:
           return False

    def validMoves(self, row: int, col: int, board: list[list]) -> list[(int, int)]:
        return []
    
    def makeMove(self, oldRow, oldCol, newRow, newCol, sqrSize, sqrX1, sqrY1, piecesTaken, board, canvas):
        piece: Piece = board[oldRow][oldCol]
        self.isMoved = True
        # take piece if its different color
        if board[newRow][newCol] != None:
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
            self.path = "chess/img/pawnB.png"
        else:
            self.path = "chess/img/pawnW.png"
    
    def validMoves(self, row: int, col: int, board: list[list]) -> list[(int, int)]:
        res = []
        if self.color == "b":
            if board[row+1][col] == None:
                res.append((row+1, col))
            if (self.isMoved == False) and board[row+1][col] == None and board[row+2][col] == None:
                res.append((row+2, col))
                
            if col + 1 < 8 and board[row+1][col+1] != None and board[row+1][col+1].color != "b":
                res.append((row+1, col+1))
            if col - 1 > -1 and board[row+1][col-1] != None and board[row+1][col-1].color != "b":
                res.append((row+1, col-1))
                
        else:
            if board[row-1][col] == None:
                res.append((row-1, col))
            if (not self.isMoved) and board[row-1][col] == None and board[row-2][col] == None:
                res.append((row-2, col))
            if col + 1 < 8 and board[row-1][col+1] != None and board[row-1][col+1].color != "w":
                res.append((row-1, col+1))
            if col - 1 > -1 and board[row-1][col-1] != None and board[row-1][col-1].color != "w":
                res.append((row-1, col-1))
        return res
        

class Rook(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        if color == "b":
            self.path = "chess/img/rookB.png"
        else:
            self.path = "chess/img/rookW.png"

    def validMoves(self, row: int, col: int, board: list[list]) -> list[(int, int)]:
         res = []
         moves = [(0,-1),(0,1),(1,0),(-1,0)]
         for mRow, mCol in moves:
             for i in range(1,8):
                 newRow = row + (i*mRow)
                 newCol = col + (i*mCol)
                 if self.checkFreeSpace(newRow, newCol, board):
                     res.append((newRow, newCol))
                     if board[newRow][newCol] != None and board[newRow][newCol].color != self.color:
                         break
                 else:
                     break
         return res


class Knight(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        if color == "b":
            self.path = "chess/img/knightB.png"
        else:
            self.path = "chess/img/knightW.png"
    
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
            self.path = "chess/img/bishopB.png"
        else:
            self.path = "chess/img/bishopW.png"
    
    def validMoves(self, row: int, col: int, board: list[list]) -> list[(int, int)]:
        res = []
        moves = [(1,1),(1,-1),(-1,-1),(-1,1)]
        for mRow, mCol in moves:
            for i in range(1,8):
                newRow = row + (i*mRow)
                newCol = col + (i*mCol)
                if self.checkFreeSpace(newRow, newCol, board):
                    res.append((newRow, newCol))
                    if board[newRow][newCol] != None and board[newRow][newCol].color != self.color:
                        break
                else:
                    break
        return res
    

class Queen(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        if color == "b":
            self.path = "chess/img/queenB.png"
        else:
            self.path = "chess/img/queenW.png"

    def validMoves(self, row: int, col: int, board: list[list]) -> list[(int, int)]:
        res = []
        moves = [(0,-1),(0,1),(1,0),(-1,0), (1,1),(1,-1),(-1,-1),(-1,1)]
        for mRow, mCol in moves:
            for i in range(1,8):
                newRow = row + (i*mRow)
                newCol = col + (i*mCol)
                if self.checkFreeSpace(newRow, newCol, board):
                    res.append((newRow, newCol))
                    if board[newRow][newCol] != None and board[newRow][newCol].color != self.color:
                        break
                else:
                    break
        return res

class King(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        if color == "b":
            self.path = "chess/img/kingB.png"
        else:
            self.path = "chess/img/kingW.png"

    def validMoves(self, row: int, col: int, board: list[list]) -> list[(int, int)]:
        res = []
        moves = [(-1,0),(-1,1),(-1,-1),(0,-1),(0,1),(1,1),(1,0),(1,-1)]
        for mRow, mCol in moves:
            if self.checkFreeSpace(row+mRow, col+mCol, board):
                res.append((row+mRow, col+mCol))
        return res

