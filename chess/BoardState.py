import tkinter

class BoardState:
    def __init__(self, canvas) -> None:
        self.player = "b"
        self.pos = None
        self.isPicking = True
        self.canvas: tkinter.Canvas = canvas
        self.piecesTaken = {
            "b": [],
            "w": []
        }
    
    def setColor(self, r, g ,b):
        color = f'#{r:02x}{g:02x}{b:02x}'
        return color
    
    def setTurn(self):
        self.player = "w" if self.player == "b" else "b"
        if self.player == "w":
            self.canvas.itemconfig(tagOrId="white", font=("Verdana", self.sqrSize//4, "bold"))
            self.canvas.itemconfig(tagOrId="black", font=("Verdana", self.sqrSize//4))
        else:
            self.canvas.itemconfig(tagOrId="black", font=("Verdana", self.sqrSize//4, "bold"))
            self.canvas.itemconfig(tagOrId="white", font=("Verdana", self.sqrSize//4))


    def drawStats(self, offsetX1, offsetY1, offsetX2, offsetY2, sqrSize):
        self.canvas.create_rectangle(offsetX1, offsetY1,offsetX2, offsetY2,)
        self.offset = offsetY1
        self.sqrSize = sqrSize
        self.canvas.create_text(offsetX1 + sqrSize//1.5, offsetY1 + sqrSize//4, text="Black", 
                           font=("Verdana", sqrSize//4), tags="black", fill=self.setColor(84, 60, 199))
        self.canvas.create_text(offsetX1 + sqrSize//1.5, offsetY2 - sqrSize//4, text="White", 
                           font=("Verdana", sqrSize//4), tags="white", fill=self.setColor(242, 130, 104))
        
    def showTaken(self):
        bRowCounter = -1
        for i, piece in enumerate(self.piecesTaken["b"]):
            if i % 7 == 0:
                bRowCounter += 1
            self.canvas.coords(piece.imgId, self.sqrSize*9.55 + (i%7)*(self.sqrSize - self.sqrSize*0.35), self.sqrSize//0.8 + bRowCounter*self.sqrSize)
        wRowCounter = -1
        for j, piece in enumerate(self.piecesTaken["w"]):
            if j % 7 == 0:
                wRowCounter += 1
            self.canvas.coords(piece.imgId, self.sqrSize*9.55 + (j%7)*(self.sqrSize - self.sqrSize*0.35), self.sqrSize*7.85 - wRowCounter*self.sqrSize)