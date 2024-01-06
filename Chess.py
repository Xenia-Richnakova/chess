import tkinter
from Pieces import *
from BoardState import *
from PIL import Image, ImageTk

class Board:
    def __init__(self) -> None:
        self.size = 70
        self.label = 20
        self.root = tkinter.Tk()
        self.canWidth = self.size*8+(4*self.label) + self.size*5
        self.canHeight = self.size*8+(4*self.label)
        self.canvas = tkinter.Canvas(self.root, width=self.canWidth, height=self.canHeight)
        self.offset = self.label*2
        self.canvas.pack()

        self.board = self.initBoard()
        self.boardState = BoardState(self.canvas, self)
        self.introImage(self.initDraw)
        # lighted squares colors
        self.ligtWhite = self.changeCol(*tuple(int(c * 0.4 + 255 * 0.6) for c in (102, 216, 185)))
        self.ligtBlack = self.changeCol(*tuple(int(c * 0.4 + 255 * 0.6) for c in (5, 255, 5)))

    def initBoard(self) -> list[list[Piece]]: 
        return [[Rook("b"), Knight("b"), Bishop("b"), Queen("b"), King("b"), Bishop("b"), Knight("b"), Rook("b")],
                [Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b')],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w')],
                [Rook('w'), Knight("w"), Bishop("w"), Queen("w"), King("w"), Bishop("w"), Knight("w"), Rook("w")]]
        

    def lightsOn(self, squares: list):
        for row, col in squares:
            color = self.canvas.itemcget(f"{row},{col}", "fill")
            if color == self.white:
                self.canvas.itemconfig(f"{row},{col}", fill=self.ligtWhite)
            else:
                self.canvas.itemconfig(f"{row},{col}", fill=self.ligtBlack)

    def lightsOff(self, squares: list):
        for row, col in squares:
            color = self.canvas.itemcget(f"{row},{col}", "fill")
            if color == self.ligtWhite:
                self.canvas.itemconfig(f"{row},{col}", fill=self.white)
            else:
                self.canvas.itemconfig(f"{row},{col}", fill=self.black)

    
    def handleSqr(self, row, col, x, y):
        if self.boardState.isPicking:
            piece = self.board[row][col]
            if self.board[row][col] == None or piece.color != self.boardState.player:
                return
            self.boardState.pos = (row, col)
            self.boardState.isPicking = False

            # light squares
            validSqr = piece.validMoves(row, col, self.board)
            self.lightsOn(validSqr)
        else:
            if self.boardState.pos == None:
                return
            oldRow, oldCol = self.boardState.pos
            if col == oldCol and row == oldRow:
                return
            oldPiece: Piece = self.board[oldRow][oldCol]
            validSqr = oldPiece.validMoves(oldRow, oldCol, self.board)
            if (row, col) in validSqr:
                # lights off
                self.lightsOff(validSqr)
                self.boardState.isPicking = True
                # move piece
                oldPiece.makeMove(oldRow, oldCol, row, col, self.size, x, y, self.boardState.piecesTaken ,self.board, self.canvas)
                # display taken pieces
                self.boardState.showTaken()
                # Promote pieces
                def promotion(color, row, col):
                    self.boardState.pawnPromotion(color, row, col, x, y)
                oldPiece.pawnOnOppositeSide(self.boardState.gameOver[0], self.board, promotion)
                
                #change player
                self.boardState.setTurn()
            else:
                #lights off
                self.lightsOff(validSqr)
                self.boardState.isPicking = True
                self.boardState.pos = None

        

    def handle_click(self, event):
        if self.boardState.gameOver[0] == False:
            col = event.x
            row = event.y
            for x1, y1, x2, y2, pos in self.boardPos:
                if col >= x1 and col <= x2 and row >= y1 and row <= y2:
                    self.handleSqr(pos[0], pos[1], x1, y1)

    def changeCol(self, r, g ,b):
        color = f'#{r:02x}{g:02x}{b:02x}'
        return color
    
    def introImage(self, drawBoard):
        begin = Image.open('chess/img/LetsBegin.png')
        begin = begin.resize((6*self.size, 6*self.size))
        self.begin = ImageTk.PhotoImage(begin)
        self.canvas.create_image(self.canWidth//2, self.canHeight//2, image=self.begin, tags="beginImg")
        def f():
            self.canvas.delete("beginImg")
            drawBoard()
        self.root.after(4000, f)
    
    def initDraw(self):
        #border
        self.canvas.create_rectangle(self.label, self.label, 8*self.size + self.label*3, 8*self.size + self.label*3)
        # square colors 
        self.white = self.changeCol(247, 230, 225)
        self.black = self.changeCol(135, 60, 250)
        
        # creating squares 
        for row in range(8):
            if row % 2 == 0:
                color = self.white
            else:
                color = self.black
            for col in range(8):
                self.canvas.create_rectangle(col*self.size+self.offset, row*self.size+self.offset, 
                                             col*self.size+self.size+self.offset, row*self.size+self.size+self.offset, 
                                             fill=color, outline="", tags=f"{row},{col}")
                if color == self.white:
                    color = self.black
                else:
                    color = self.white
                
        letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        nums = [8, 7, 6, 5, 4, 3, 2, 1]
        # writing labels
        for col in range(8):
            # letters up and down 
            self.canvas.create_text(col*(self.size)+self.offset+self.size/2, self.offset-self.label/2, text=letters[col])
            self.canvas.create_text(col*(self.size)+self.offset+self.size/2, self.offset+self.label/2+(self.size*8), text=letters[col])
            # numbers left and right
            self.canvas.create_text(self.offset-self.label/2, (col*self.size)+self.size/2+self.offset, text=nums[col])
            self.canvas.create_text(self.offset+self.size*8+self.label/2, (col*self.size)+self.size/2+self.offset, text=nums[col])
        
        self.canvas.create_rectangle(self.offset, self.offset, self.offset+self.size*8, self.offset+self.size*8)

        self.boardPos = []
        self.pieces = []
        for row in range(8):
            for col in range(8):
                self.boardPos.append((col*self.size+self.offset, row*self.size+self.offset, col*self.size+self.size+self.offset, row*self.size+self.size+self.offset, (row, col)))
                obj = self.board[row][col]
                if obj != None:
                    self.pieces.append(obj.tkImage(self.size - self.size * 0.1))
                    pImg = self.canvas.create_image(self.offset+(col*self.size) + self.size/2, self.offset+(row*self.size) + self.size/2, image=self.pieces[-1])
                    self.board[row][col].imgId = pImg

        
        # Stats
        self.boardState.drawStats(self.size*8+(4*self.label), self.label, self.size*8+(3*self.label) + self.size*5, self.size*8+(3*self.label), self.size)
        self.boardState.setTurn()

class Program:
    def __init__(self):
        self.b = Board()
        self.b.canvas.bind("<Button-1>", self.b.handle_click)
        tkinter.mainloop()

    ...

Program()

