import tkinter
from Pieces import *


class BoardState:
    def __init__(self, canvas, mainBoard) -> None:
        self.mainBoard = mainBoard
        self.player = "b"
        self.pos = None
        self.isPicking = True
        self.canvas: tkinter.Canvas = canvas
        self.gameOver = [False, "color"]
        self.piecesTaken = {
            "b": [],
            "w": []
        }
        self.score = self.readScore()
    
    def setColor(self, r, g ,b):
        color = f'#{r:02x}{g:02x}{b:02x}'
        return color
    
    def setTurn(self):
        self.player = "w" if self.player == "b" else "b"
        if self.player == "w":
            self.canvas.itemconfig(tagOrId="white", 
                                   font=("Verdana", self.sqrSize//4, "bold"))
            self.canvas.itemconfig(tagOrId="black", 
                                   font=("Verdana", self.sqrSize//4))
        else:
            self.canvas.itemconfig(tagOrId="black", 
                                   font=("Verdana", self.sqrSize//4, "bold"))
            self.canvas.itemconfig(tagOrId="white", 
                                   font=("Verdana", self.sqrSize//4))


    def drawStats(self, offsetX1, offsetY1, offsetX2, offsetY2, sqrSize):
        self.canvas.create_rectangle(offsetX1, offsetY1,offsetX2, offsetY2,)
        self.offset = offsetY1
        self.sqrSize = sqrSize
        self.canvas.create_text(offsetX1 + sqrSize//1.5, offsetY1 + sqrSize//4, 
                                text="Black", 
                           font=("Verdana", sqrSize//4), tags="black", 
                           fill=self.setColor(84, 60, 199))
        self.canvas.create_text(offsetX1 + 3.7 * sqrSize, offsetY1 + sqrSize//4, 
                                text=f"Won: {self.score['black']}", 
                           font=("Verdana", sqrSize//4), 
                           fill=self.setColor(84, 60, 199))
        self.canvas.create_text(offsetX1 + sqrSize//1.5, offsetY2 - sqrSize//4, 
                                text="White", 
                           font=("Verdana", sqrSize//4), tags="white", 
                           fill=self.setColor(242, 130, 104))
        self.canvas.create_text(offsetX1 + 3.7 * sqrSize, offsetY2 - sqrSize//4, 
                                text=f"Won: {self.score['white']}", 
                           font=("Verdana", sqrSize//4), 
                           fill=self.setColor(242, 130, 104))
        
    def showTaken(self):
        bRowCounter = -1
        for i, piece in enumerate(self.piecesTaken["b"]):
            if isinstance(piece, King):
                self.gameOver[0] = True
                self.gameOver[1] = "w"
                self.endGame()
            if i % 7 == 0:
                bRowCounter += 1
            self.canvas.coords(piece.imgId, self.sqrSize * 9.55 + (i%7) * 
                               (self.sqrSize - self.sqrSize * 0.35), 
                               self.sqrSize//0.8 + bRowCounter * self.sqrSize)
        wRowCounter = -1
        for j, piece in enumerate(self.piecesTaken["w"]):
            if isinstance(piece, King):
                self.gameOver[0] = True
                self.gameOver[1] = "b"
                self.endGame()
            if j % 7 == 0:
                wRowCounter += 1
            self.canvas.coords(piece.imgId, self.sqrSize * 9.55 + (j%7) * 
                               (self.sqrSize - self.sqrSize * 0.35), 
                               self.sqrSize * 7.85 - wRowCounter * self.sqrSize)
    
    def pawnPromotion(self, color, row, col, x, y):
        self.gameOver[0] = True
        piecesDialog = tkinter.Toplevel(self.canvas)
        piecesDialog.title("Promotion")
        self.promotedPieces = []
        p = [Rook(color), Bishop(color), Knight(color), Queen(color)]
        def pickPiece(piece: Piece):
            self.canvas.delete(self.mainBoard.board[row][col].imgId)
            self.mainBoard.board[row][col] = piece
            fig = piece.tkImage(self.sqrSize - self.sqrSize * 0.1)
            self.mainBoard.pieces.append(fig)
            piece.imgId = self.canvas.create_image(x + self.sqrSize//2, 
                                                   y + self.sqrSize//2, 
                                                   image=fig)
            piecesDialog.destroy()
            self.gameOver[0] = False
        # pieces in buttons
        self.promotedPieces.append(p[0].tkImage(self.sqrSize))
        button = tkinter.Button(piecesDialog, image=self.promotedPieces[0], 
                                command=lambda: pickPiece(p[0]))
        button.pack(side=tkinter.LEFT, padx=5, pady=5)

        self.promotedPieces.append(p[1].tkImage(self.sqrSize))
        button = tkinter.Button(piecesDialog, image=self.promotedPieces[1], 
                                command=lambda: pickPiece(p[1]))
        button.pack(side=tkinter.LEFT, padx=5, pady=5)

        self.promotedPieces.append(p[2].tkImage(self.sqrSize))
        button = tkinter.Button(piecesDialog, image=self.promotedPieces[2], 
                                command=lambda: pickPiece(p[2]))
        button.pack(side=tkinter.LEFT, padx=5, pady=5)

        self.promotedPieces.append(p[3].tkImage(self.sqrSize))
        button = tkinter.Button(piecesDialog, image=self.promotedPieces[3], 
                                command=lambda: pickPiece(p[3]))
        button.pack(side=tkinter.LEFT, padx=5, pady=5)
    
    def setNewGame(self):
        self.canvas.delete("all")
        self.mainBoard.board = self.mainBoard.initBoard()
        self.mainBoard.initDraw()
        self.gameOver = [False, "color"]
        self.piecesTaken = {
            "b": [],
            "w": []
        }
        self.removeButton()

    def removeButton(self):
        if self.gameOver[0] == False:
            self.playAgain.destroy()

    def readScore(self):
        with open("./score.txt", "r") as f:
            file = f.readlines()
        b = file[0].split(":")
        w = file[1].split(":")
        score = {
            "black": int(b[1].replace("\n", "")[1:]),
            "white": int(w[1][1:])
        }
        return score
    
    def writeScore(self, color):
        open("./score.txt", 'w').close()
        with open("./score.txt", "w") as f:
            if color == "w":
                self.score['white'] = self.score['white'] + 1
            else:
                self.score['black'] = self.score['black'] + 1
            f.write(f"Black: {self.score['black']}\nWhite: {self.score['white']}")

    def openAnim(self, pieceImg, num):
        self.width = self.sqrSize*8+(4*self.offset)
        self.height = self.sqrSize*8+(4*self.offset)
        self.canvas.create_image(self.width//2, self.height//2, 
                                 image=pieceImg, tags=f"king{num}")

    def showNext(self, oldIndex, max):
        self.canvas.delete(f"king{oldIndex}")
        if oldIndex == max:
            return
        self.openAnim(self.winnerImages[oldIndex], oldIndex+1)
        self.mainBoard.root.after(400, lambda: self.showNext(oldIndex+1, max))

    def winnerDance(self, winCol):
        self.winnerImages: list = []
        for i in range(1,10):
            img = Image.open(f"./anim/king{winCol}_{i}.png")
            img = img.resize((self.sqrSize*2, self.sqrSize*2))
            pieceImg = ImageTk.PhotoImage(img)
            self.winnerImages.append(pieceImg)
        self.openAnim(self.winnerImages[0], 1)
        self.mainBoard.root.after(400, lambda: self.showNext(1, 9))

    def endGame(self):
        if self.gameOver[1] == "w":
            self.writeScore("w")
            self.winnerDance("W")
        elif self.gameOver[1] == "b":
            self.writeScore("b")
            self.winnerDance("B")
        self.btn = ImageTk.PhotoImage(file="./img/button_play-again.png")
        self.playAgain = tkinter.Button(self.mainBoard.root, image=self.btn, 
                                        border=0, command=self.setNewGame)
        self.playAgain.place(x=self.width//8 + self.width, y=self.height//2)

        