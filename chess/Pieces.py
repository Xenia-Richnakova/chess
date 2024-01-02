from PIL import Image, ImageTk

class Piece:
    def __init__(self, color: str) -> None:
        self.color = color
        self.imgId = None
        self.isMoved = False

    def validMoves(self, row: int, col: int, board: list[list]) -> list[(int, int)]:
        return []

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
            if (not self.isMoved) and board[row+1][col] == None and board[row+2][col] == None:
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
    


class Knight(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        if color == "b":
            self.path = "chess/img/knightB.png"
        else:
            self.path = "chess/img/knightW.png"

class Bishop(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        if color == "b":
            self.path = "chess/img/bishopB.png"
        else:
            self.path = "chess/img/bishopW.png"

class Queen(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        if color == "b":
            self.path = "chess/img/queenB.png"
        else:
            self.path = "chess/img/queenW.png"

class King(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        if color == "b":
            self.path = "chess/img/kingB.png"
        else:
            self.path = "chess/img/kingW.png"

