import sys, os
import pygame
import pygame.mixer as Mixer
pygame.init()

"""VARIABLES, CONSTANTS, OBJECTS"""
#WINDOW
WIDTH = 900
HEIGHT = 720
title = "Chess by Matte"

#GRAPHICS
FPS = 60
BTNPRESS = FPS/2
clock = pygame.time.Clock()

SQUARE = 82
BORDER = 34
PIECE = 80

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BTNW = 150
BTNH = 50

#GAME
pieceslist = []
position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
positionset = []
wturn = True
rot = 1
advantage = 0

#SPRITESHEETS
#-----PIECES
stylenumber = 1
def refreshstyle():
    global pawns, bishops, knights, rooks, queens, kings
    pawns = [pygame.image.load("res/white" + str(stylenumber) + "/pawn.png"), pygame.image.load("res/black" + str(stylenumber) + "/pawn.png")]
    bishops = [pygame.image.load("res/white" + str(stylenumber) + "/bishop.png"), pygame.image.load("res/black" + str(stylenumber) + "/bishop.png")]
    knights = [pygame.image.load("res/white" + str(stylenumber) + "/knight.png"), pygame.image.load("res/black" + str(stylenumber) + "/knight.png")]
    rooks = [pygame.image.load("res/white" + str(stylenumber) + "/rook.png"), pygame.image.load("res/black" + str(stylenumber) + "/rook.png")]
    queens = [pygame.image.load("res/white" + str(stylenumber) + "/queen.png"), pygame.image.load("res/black" + str(stylenumber) + "/queen.png")]
    kings = [pygame.image.load("res/white" + str(stylenumber) + "/king.png"), pygame.image.load("res/black" + str(stylenumber) + "/king.png")]
refreshstyle()

#-----PIECES ICONS
iconsize = (20, 20)
bishopsicons = [pygame.transform.scale(bishops[0], iconsize), pygame.transform.scale(bishops[1], iconsize)]
knightsicons = [pygame.transform.scale(knights[0], iconsize), pygame.transform.scale(knights[1], iconsize)]
rooksicons = [pygame.transform.scale(rooks[0], iconsize), pygame.transform.scale(rooks[1], iconsize)]
queensicons = [pygame.transform.scale(queens[0], iconsize), pygame.transform.scale(queens[1], iconsize)]

#-----BOARDS
boardnumber = 0
boards = [pygame.image.load("res/boards/board01.jpg"), pygame.image.load("res/boards/board02.jpg"), pygame.image.load("res/boards/board03.jpg")]
undoboards = [pygame.image.load("res/boards/undo01.jpg"), pygame.image.load("res/boards/undo02.jpg"), pygame.image.load("res/boards/undo03.jpg")]

#-----BUTTONS
buttons = [pygame.image.load("res/buttons/ChangeBoard.png"), pygame.image.load("res/buttons/Reset.png"), pygame.image.load("res/buttons/Rotate.png"), pygame.image.load("res/buttons/Undo.png"), pygame.image.load("res/buttons/Redo.png"), pygame.image.load("res/buttons/ChangeStyle.png")]
pressedbuttons = [pygame.image.load("res/buttons/ChangeBoardPressed.png"), pygame.image.load("res/buttons/ResetPressed.png"), pygame.image.load("res/buttons/RotatePressed.png"), pygame.image.load("res/buttons/UndoPressed.png"), pygame.image.load("res/buttons/RedoPressed.png"), pygame.image.load("res/buttons/ChangeStylePressed.png")]

#-----OTHER
checkbg = pygame.image.load("res/checkbg.png")
possmov = pygame.image.load("res/point.png")
posseat = pygame.image.load("res/circle.png")

#SOUNDS
movesound = Mixer.Sound("res/sounds/move.wav")
capturesound = Mixer.Sound("res/sounds/capture.wav")
checksound = Mixer.Sound("res/sounds/check.wav")
castlesound = Mixer.Sound("res/sounds/castle.wav")

donesound = False

"""WINDOW INITIALIZATION"""
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(title)
pygame.display.set_icon(pygame.image.load("res/icon.ico"))

"""RENDERING FUNCTIONS"""
#---------------------------------------------
def drawgame():
    win.fill(WHITE)    
    if undocount <= 1: win.blit(boards[boardnumber], (0, 0))
    else: win.blit(undoboards[boardnumber], (0, 0))

    drawmovenumber(win)
    drawadvantage(win)
    drawturn(win)

    drawboardchoice(win)
    drawstylechoice(win)
    drawreset(win)
    drawrotate(win)
    drawundo(win)
    drawredo(win)

    drawpromotionchoice(win)
    
    drawpieces(win)

    pygame.display.update()
#---------------------------------------------
#TEXTS
def drawmovenumber(win):
    font = pygame.font.SysFont('Arial', 20)
    txt = font.render("Move number: " + str(len(positionset)-undocount), False, BLACK) #current turn
    win.blit(txt, (5, 5))
def drawadvantage(win):
    font = pygame.font.SysFont('Arial', 20)
    txt = font.render("Advantage: " + str(advantage), False, BLACK) #current turn
    win.blit(txt, (150, 5))
def drawturn(win):
    if wturn: tmp = "white"
    else: tmp = "black"

    font = pygame.font.SysFont('Arial', 20)
    txt = font.render("Turn: " + tmp, False, BLACK) #current turn
    win.blit(txt, (280, 5))
#---------------------------------------------
#BUTTONS
bctimer = 0
def drawboardchoice(win):
    global bctimer
    if btnboardchoice.pressed:
        btnboardchoice.which = pressedbuttons[0]
        if bctimer >= BTNPRESS:
            bctimer = 0
            btnboardchoice.pressed = False
        bctimer += 1
    else: btnboardchoice.which = buttons[0]
    btnboardchoice.renderbutton(win, 730, 10)
styletimer = 0
def drawstylechoice(win):
    global styletimer
    if btnstylechoice.pressed:
        btnstylechoice.which = pressedbuttons[5]
        if styletimer >= BTNPRESS:
            styletimer = 0
            btnstylechoice.pressed = False
        styletimer += 1
    else: btnstylechoice.which = buttons[5]
    btnstylechoice.renderbutton(win, 730, 70)
restimer = 0
def drawreset(win):
    global restimer
    if btnreset.pressed:
        btnreset.which = pressedbuttons[1]
        if restimer >= BTNPRESS:
            restimer = 0
            btnreset.pressed = False
        restimer += 1
    else: btnreset.which = buttons[1]
    btnreset.renderbutton(win, 730, 130)
rottimer = 0
def drawrotate(win):
    global rottimer
    if btnrotate.pressed:
        btnrotate.which = pressedbuttons[2]
        if rottimer >= BTNPRESS:
            rottimer = 0
            btnrotate.pressed = False
        rottimer += 1
    else: btnrotate.which = buttons[2]
    btnrotate.renderbutton(win, 730, 190)
undotimer = 0
def drawundo(win):
    global undotimer
    if btnundo.pressed:
        btnundo.which = pressedbuttons[3]
        if undotimer >= BTNPRESS:
            undotimer = 0
            btnundo.pressed = False
        undotimer += 1
    else: btnundo.which = buttons[3]
    btnundo.renderbutton(win, 725, 250)
redotimer = 0
def drawredo(win):
    global redotimer
    if btnredo.pressed:
        btnredo.which = pressedbuttons[4]
        if redotimer >= BTNPRESS:
            redotimer = 0
            btnredo.pressed = False
        redotimer += 1
    else: btnredo.which = buttons[4]
    btnredo.renderbutton(win, 730 + BTNW/2 + 5, 250)
#---------------------------------------------
#OTHER
wpromotion = queens[0]
bpromotion = queens[1]
def drawpromotionchoice(win):
    font = pygame.font.SysFont('Arial', 18)

    txt = font.render("White promotion:", False, BLACK)
    win.blit(txt, (WIDTH - 170, HEIGHT - 120))

    txt = font.render("Black promotion:", False, BLACK)
    win.blit(txt, (WIDTH - 170, HEIGHT - 60))

    pygame.draw.rect(win, (200, 200, 200), (WIDTH - 170, HEIGHT - 40, 160, 30))
    pygame.draw.rect(win, (200, 200, 200), (WIDTH - 170, HEIGHT - 100, 160, 30))

    #white icons
    win.blit(queensicons[0], (WIDTH-165, HEIGHT-95))
    win.blit(rooksicons[0], (WIDTH-140, HEIGHT-94))
    win.blit(bishopsicons[0], (WIDTH-115, HEIGHT-94))
    win.blit(knightsicons[0], (WIDTH-90, HEIGHT-94))

    win.blit(pygame.transform.scale(wpromotion, (25, 25)), (WIDTH-40, HEIGHT-97))

    #black icons 
    win.blit(queensicons[1], (WIDTH-165, HEIGHT-35))
    win.blit(rooksicons[1], (WIDTH-140, HEIGHT-34))
    win.blit(bishopsicons[1], (WIDTH-115, HEIGHT-34))
    win.blit(knightsicons[1], (WIDTH-90, HEIGHT-34))

    win.blit(pygame.transform.scale(bpromotion, (25, 25)), (WIDTH-40, HEIGHT-37))
def drawpieces(win):
    for i in pieceslist:
        if not i == "none":
            i.draw(win)

"""UTILS FUNCTIONS"""
#INPUT: square's row and column
#OUTPUT: square's x and y for spritesheets placing
def squarepos(row, column):
    return (BORDER + SQUARE*column - SQUARE/2 - PIECE/2, BORDER + SQUARE*row - SQUARE/2 - PIECE/2)

#INPUT: x and y coordinates
#OUTPUT: [row, column] of the square if on the board / null if outside of the board
def getsquare(x, y):
    if x <= BORDER or y <= BORDER or x >= squarepos(1,  9)[0] or y >= squarepos(9, 1)[1]:
        pass #not on the board
    else:
        x -= BORDER
        y -= BORDER
        x /= SQUARE
        y /= SQUARE
        return [int(x) + 1, int(y) + 1]

#INPUT: 0 - 63 square's board position
#OUTPUT: [row, column] of the square
def findsquare(n):
    return [int(n/8) + 1, n%8 + 1]

#INPUT: square's [row, column]
#OUTPUT: 0 - 63 square's board position
#WARNING: USE CAREFULLY, BAD FUNCTION (not a fixable problem, just debug a lot when using) (inversion of row-column input)
def findsquareposition(row, column):
    return (column - 1)*8 + row - 1

"""OTHER FUNCTIONS"""
#resets the game to its default position
def reset():
    global position, wturn, positionset, undocount, rot
    position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    positionset.clear()
    positionset.append(position)
    wturn = True
    undocount = 1
    rot = 1
    defBoardPieces()
    calcAdvantage()

#fills with objects and "none" strings in pieceslist list from index 0 to 63 relying on position string
def defBoardPieces():
    global pieceslist
    pieceslist.clear()
    tmp = position.replace("/", "")
    pos = 0
    for i in tmp:
        if i.isnumeric():
            for j in range(int(i)):
                pieceslist.append("none")
                pos += 1
        else:
            if i == "p": pieceslist.append(piece(squarepos(findsquare(pos)[0], findsquare(pos)[1])[0], squarepos(findsquare(pos)[0], findsquare(pos)[1])[1], "pawn", "black"))
            elif i == "P": pieceslist.append(piece(squarepos(findsquare(pos)[0], findsquare(pos)[1])[0], squarepos(findsquare(pos)[0], findsquare(pos)[1])[1], "pawn", "white"))
            elif i == "n": pieceslist.append(piece(squarepos(findsquare(pos)[0], findsquare(pos)[1])[0], squarepos(findsquare(pos)[0], findsquare(pos)[1])[1], "knight", "black"))
            elif i == "N": pieceslist.append(piece(squarepos(findsquare(pos)[0], findsquare(pos)[1])[0], squarepos(findsquare(pos)[0], findsquare(pos)[1])[1], "knight", "white"))
            elif i == "b": pieceslist.append(piece(squarepos(findsquare(pos)[0], findsquare(pos)[1])[0], squarepos(findsquare(pos)[0], findsquare(pos)[1])[1], "bishop", "black"))
            elif i == "B": pieceslist.append(piece(squarepos(findsquare(pos)[0], findsquare(pos)[1])[0], squarepos(findsquare(pos)[0], findsquare(pos)[1])[1], "bishop", "white"))
            elif i == "r": pieceslist.append(piece(squarepos(findsquare(pos)[0], findsquare(pos)[1])[0], squarepos(findsquare(pos)[0], findsquare(pos)[1])[1], "rook", "black"))
            elif i == "R": pieceslist.append(piece(squarepos(findsquare(pos)[0], findsquare(pos)[1])[0], squarepos(findsquare(pos)[0], findsquare(pos)[1])[1], "rook", "white"))
            elif i == "q": pieceslist.append(piece(squarepos(findsquare(pos)[0], findsquare(pos)[1])[0], squarepos(findsquare(pos)[0], findsquare(pos)[1])[1], "queen", "black"))
            elif i == "Q": pieceslist.append(piece(squarepos(findsquare(pos)[0], findsquare(pos)[1])[0], squarepos(findsquare(pos)[0], findsquare(pos)[1])[1], "queen", "white"))
            elif i == "k": pieceslist.append(piece(squarepos(findsquare(pos)[0], findsquare(pos)[1])[0], squarepos(findsquare(pos)[0], findsquare(pos)[1])[1], "king", "black"))
            elif i == "K": pieceslist.append(piece(squarepos(findsquare(pos)[0], findsquare(pos)[1])[0], squarepos(findsquare(pos)[0], findsquare(pos)[1])[1], "king", "white"))
            pos += 1

#fills position string relying on pieceslist list
def refreshPositions():
    global position
    position = ""
    empty = 0
    for i in range(64):
        tmp = pieceslist[i]
        if i%8 == 0 and i != 0:
            if empty != 0:
                position += str(empty)
                empty = 0
            position += "/"
        if tmp == "none":
            empty += 1
        else:
            if empty != 0:
                position += str(empty)
                empty = 0
            if tmp.img == pawns[0]: position += "P"
            elif tmp.img == pawns[1]: position += "p"
            elif tmp.img == knights[0]: position += "N"
            elif tmp.img == knights[1]: position += "n"
            elif tmp.img == bishops[0]: position += "B"
            elif tmp.img == bishops[1]: position += "b"
            elif tmp.img == rooks[0]: position += "R"
            elif tmp.img == rooks[1]: position += "r"
            elif tmp.img == queens[0]: position += "Q"
            elif tmp.img == queens[1]: position += "q"
            elif tmp.img == kings[0]: position += "K"
            elif tmp.img == kings[1]: position += "k"
            else: print("error")
    if empty != 0: position += str(empty)
    #print(position)

#rotates the board by reversing position string and by swapping promotion choice variables
def rotate():
    global position, positionset, rot

    position = position[::-1]

    defBoardPieces()

    if rot == 1: rot = -1
    else: rot = 1

#calculates game's advantage relying on pieceslist
def calcAdvantage():
    global advantage
    tmp = 0
    for i in pieceslist:
        if i != "none":
            if i.img == pawns[0]: tmp += 1
            elif i.img == pawns[1]: tmp -= 1
            elif i.img == knights[0] or i.img == bishops[0]: tmp += 3
            elif i.img == knights[1] or i.img == bishops[1]: tmp -= 3
            elif i.img == rooks[0]: tmp += 5
            elif i.img == rooks[1]: tmp -= 5
            elif i.img == queens[0]: tmp += 9
            elif i.img == queens[1]: tmp -= 9
    advantage = tmp

#undo to the previous move
def undo():
    global position, wturn, undocount
    if len(positionset) > undocount:
        undocount += 1
        position = positionset[-undocount]
        if wturn: wturn = False
        else: wturn = True
        defBoardPieces()

#redo to the next Move
def redo():
    global undocount, wturn, position
    if undocount > 1:
        undocount -= 1
        position = positionset[-undocount]
        if wturn: wturn = False
        else: wturn = True
        defBoardPieces()

#INPUT: a piece object, board list
#OUTPUT: [True,  kingpos] (the piece is checking enemy's king) / [False, kingpos] (the piece isn't checking enemy's king)
def check(obj, plist):
    for i in range(64):
        if plist[i] != "none":
            if plist[i].which == "king":
                if plist[i].color != obj.color:
                    kingpos = i
                    if obj.islegalmove1(obj.square, plist[i].square) and obj.canmove(plist[i].square):
                        return [True, kingpos]
    return [False, kingpos]

"""BUTTON CLASS"""
class button(object):
    #class constructor
    #ATTRIBUTES:
    # w, h (int)
    # which (surface)
    # pressed (boolean)
    def __init__(self, w, h, which):
        self.w = w
        self.h = h
        self.which = which
        self.pressed = False  
    #renders button
    def renderbutton(self, win, x, y):
        win.blit(self.which, (x, y, self.w, self.h))

#BUTTON OBJECTS
btnboardchoice = button(BTNW, BTNH, buttons[0])
btnreset = button(BTNW, BTNH, buttons[1])
btnrotate = button(BTNW, BTNH, buttons[2])
btnundo = button(BTNW, BTNH, buttons[3])
btnredo = button(BTNW, BTNH, buttons[4])
btnstylechoice = button(BTNW, BTNH, buttons[5])

"""PIECE CLASS"""
class piece(object):
    #constructor method
    #ATTRIBUTES:
    # x, y (int)
    # which (string)
    # color (string)
    # square ([int, int])
    # dragging (boolean)
    # isfirstmove (boolean)
    # dmoved (boolean)
    # img (surface)
    # ischecked (boolean)
    def __init__(self, x, y, which, color):
        self.x = x
        self.y = y
        self.which = which
        self.color = color
        self.square = getsquare(x + PIECE/2, y + PIECE/2)
        self.dragging = False
        self.isfirstmove = True
        self.dmoved = False
        self.ischecked = False

        if self.which == "pawn":
            if self.color == "white": self.img = pawns[0]
            elif self.color == "black": self.img = pawns[1]
        elif self.which == "knight":
            if self.color == "white": self.img = knights[0]
            elif self.color == "black": self.img = knights[1]
        elif self.which == "bishop":
            if self.color == "white": self.img = bishops[0]
            elif self.color == "black": self.img = bishops[1]
        elif self.which == "rook":
            if self.color == "white": self.img = rooks[0]
            elif self.color == "black": self.img = rooks[1]
        elif self.which == "queen":
            if self.color == "white": self.img = queens[0]
            elif self.color == "black": self.img = queens[1]
        elif self.which == "king":
            if self.color == "white": self.img = kings[0]
            elif self.color == "black": self.img = kings[1]

    #dragging method
    def drag(self, x, y):
        limit = 720
        if x >= limit: x = limit
        self.x = x - PIECE/2
        self.y = y - PIECE/2
    
    #rendering method
    def draw(self, win):
        if self.ischecked:
            win.blit(checkbg, (self.x, self.y))
        win.blit(self.img, (self.x, self.y))
        self.square = getsquare(self.x + PIECE/2, self.y + PIECE/2)

    #INPUT: startsquare, finalsquare
    #OUTPUT: True (the move is legal) / False (the move is illegal)
    def islegalmove1(self, start, end):
        if self.canmove(start):

            if self.which == "bishop": #BISHOPS
                for i in range(1, 9):
                    if end[0] == start[0]+i and end[1] == start[1]+i: return True
                    elif end[0] == start[0]-i and end[1] == start[1]-i: return True
                    elif end[0] == start[0]+i and end[1] == start[1]-i: return True
                    elif end[0] == start[0]-i and end[1] == start[1]+i: return True
                return False

            elif self.which == "knight": #KNIGHTS
                if end[0] == start[0]+1:
                    if end[1] == start[1]+2: return True
                    elif end[1] == start[1]-2: return True
                elif end[0] == start[0]+2:
                    if end[1] == start[1]+1: return True
                    elif end[1] == start[1]-1: return True
                elif end[0] == start[0]-1:
                    if end[1] == start[1]+2: return True
                    elif end[1] == start[1]-2: return True
                elif end[0] == start[0]-2:
                    if end[1] == start[1]+1: return True
                    elif end[1] == start[1]-1: return True
                return False

            elif self.which == "queen": #QUEENS
                if end[0] == start[0] or end[1] == start[1]: return True
                for i in range(1, 9):
                    if end[0] == start[0]+i and end[1] == start[1]+i: return True
                    elif end[0] == start[0]-i and end[1] == start[1]-i: return True
                    elif end[0] == start[0]+i and end[1] == start[1]-i: return True
                    elif end[0] == start[0]-i and end[1] == start[1]+i: return True
                return False

            elif self.which == "rook": #ROOKS
                if end[0] == start[0] or end[1] == start[1]: return True
                return False

            elif self.which == "king": #KINGS
                if (end[0] == start[0]+1 and (end[1] == start[1] or end[1] == start[1]+1 or end[1] == start[1]-1)): return True
                if (end[0] == start[0] and (end[1] == start[1] or end[1] == start[1]+1 or end[1] == start[1]-1)): return True
                if (end[0] == start[0]-1 and (end[1] == start[1] or end[1] == start[1]+1 or end[1] == start[1]-1)): return True
                return False
            
            elif self.which == "pawn": #PAWNS
                if self.color == "white":
                    #NORMAL MOVE
                    if end[0] == start[0] and (end[1] == start[1]-1*rot):
                        if self.canpawnpromove(): return True
                    #DOUBLE ADVANCE MOVE
                    if end[0] == start[0] and self.isfirstmove and end[1] == start[1]-2*rot:
                        return True
                    #EN-PASSANT
                    if self.caneat(start) == "enpassant": return True
                    if self.caneat(start) == True:
                        if (end[0] == start[0]+1 or end[0] == start[0]-1) and end[1] == start[1]-1*rot: return True
                    return False
                if self.color == "black":
                    #NORMAL MOVE
                    if end[0] == start[0] and (end[1] == start[1]+1*rot):
                        if self.canpawnpromove(): return True
                    #DOUBLE ADVANCE MOVE
                    if end[0] == start[0] and self.isfirstmove and end[1] == start[1]+2*rot:
                        return True
                    #EN-PASSANT CAPTURE
                    if self.caneat(start) == "enpassant": return True
                    #NORMAL CAPTURE
                    if self.caneat(start) == True:
                        if (end[0] == start[0]+1 or end[0] == start[0]-1) and end[1] == start[1]+1*rot: return True
                    return False
        else: return False

    #INPUT: startsquare, finalsquare
    #OUTPUT: True (the move is legal) / False (the move is illegal)
    def islegalmove(self, start, end):
        if self.islegalmove1(start, end):
            #CHECK SYSTEM
            plist = pieceslist.copy()
            plist[findsquareposition(start[0], start[1])] = "none"
            plist[findsquareposition(end[0], end[1])] = self
            for el in plist:
                if el != "none":
                    if el.color != self.color:
                        ck = check(el, plist)
                        if ck[0]: return False
        else: return False
        return True

    #INPUT: startsquare
    #OUTPUT: True (the move doesn't climb any piece) / False (the move climbs another piece)
    #OTHER: castling system included
    """WARNING: MISSING CHECK CONTROLS"""
    def canmove(self, start):
        #OTHER
        for i in pieceslist:
            if i != "none" and i != self:
                if i.square == self.square:
                    #CHECKS IF THE PIECE IS OVER ANOTHER ONE OF THE SAME COLOR
                    if i.color == self.color:
                        #CASTLING SYSTEM
                        if (self.which == "king" and i.which == "rook") or (self.which == "rook" and i.which == "king"):
                            if start[1] == self.square[1]:
                                #CHECKING IF BOTH KING AND ROOK HAVEN'T MOVED YET
                                if not i.isfirstmove or not self.isfirstmove: return False

                                #CHECKING FOR INTERFERENCES BETWEEN KING AND ROOK
                                if start[0] < self.square[0]: #right
                                    for j in range(1, self.square[0] - start[0]):
                                        if pieceslist[findsquareposition(start[0] + j, self.square[1])] != "none": return False
                                if start[0] > self.square[0]: #left
                                    for j in range(1, start[0] - self.square[0]):
                                        if pieceslist[findsquareposition(start[0] - j, self.square[1])] != "none": return False

                                #ACTUAL CASTLING (MISSING CHECK CONTROLS)
                                if i.which == "rook": #king --> self
                                    if findsquare(pieceslist.index(i))[1] > 4:
                                        self.castle(self, i, "kingside")
                                    else: self.castle(self, i, "queenside")
                                elif i.which == "king": #king --> i
                                    if findsquare(pieceslist.index(self))[1] > 4:
                                        self.castle(i, self, "kingside")
                                    else: self.castle(i, self, "queenside")
                                return False 
                            #NOT AN HORIZONTAL CASTLING ATTEMPT
                            else: return False
                        #NOT ATTEMPTING TO CASTLE
                        else: return False

        #horizontal/vertical move piece climbing detection
        if start[1] == self.square[1]: #horizontal
            if start[0] < self.square[0]: #right
                for i in range(1, self.square[0] - start[0]):
                    if pieceslist[findsquareposition(start[0] + i, self.square[1])] != "none": return False
            if start[0] > self.square[0]: #left
                for i in range(1, start[0] - self.square[0]):
                    if pieceslist[findsquareposition(start[0] - i, self.square[1])] != "none": return False
        if start[0] == self.square[0]: #vertical
            if start[1] > self.square[1]: #up
                for i in range(1, start[1] - self.square[1]):
                    if pieceslist[findsquareposition(self.square[0], start[1] - i)] != "none": return False
            if start[1] < self.square[1]: #down
                for i in range(1, self.square[1] - start[1]):
                    if pieceslist[findsquareposition(self.square[0], start[1] + i)] != "none": return False
        
        #diagonal move piece climbing detection
        if self.square[1] - start[1] == self.square[0] - start[0]: #diagonal 1
            if self.square[1] - start[1] > 0: #bottom-right
                for i in range(1, self.square[1] - start[1]):
                    if pieceslist[findsquareposition(start[0], start[1])+9*i] != "none": return False
            elif self.square[1] - start[1] < 0: #top-left
                for i in range(1, start[1] - self.square[1]):
                    if pieceslist[findsquareposition(start[0], start[1])-9*i] != "none": return False
        if self.square[1] - start[1] == -(self.square[0] - start[0]): #diagonal 2
            if self.square[1] - start[1] > self.square[0] - start[0]: #bottom-left
                for i in range(1, self.square[1] - start[1]):
                    if pieceslist[findsquareposition(start[0], start[1])+7*i] != "none": return False
            if self.square[1] - start[1] < self.square[0] - start[0]: #top-right
                for i in range(1, start[1] - self.square[1]):
                    if pieceslist[findsquareposition(start[0], start[1])-7*i] != "none": return False
        
        return True

    #PAWN ONLY METHODS (no piece-type controls)
    def caneat(self, start):
        global pieceslist, donesound
        if self.color == "white":
            #                            ^      and                  (>           or                  <)
            if self.square[1] == start[1]-1*rot and (self.square[0] == start[0]+1 or self.square[0] == start[0]-1):
                for i in pieceslist:
                    if i != "none" and i != self:
                        if self.square == i.square:
                            return True
                        if i.dmoved and self.square[0] == i.square[0] and self.square[1] == i.square[1]-rot:
                            ind = pieceslist.index(i)
                            pieceslist[ind] = "none"
                            capturesound.play()
                            donesound = True
                            return "enpassant"
        elif self.color == "black":
            #                            \/     and                  (>           or                  <)
            if self.square[1] == start[1]+1*rot and (self.square[0] == start[0]+1 or self.square[0] == start[0]-1):
                for i in pieceslist:
                    if i != "none" and i != self:
                        if self.square == i.square:
                            return True
                        if i.dmoved and self.square[0] == i.square[0] and self.square[1] == i.square[1]+rot:
                            ind = pieceslist.index(i)
                            pieceslist[ind] = "none"
                            capturesound.play()
                            donesound = True
                            return "enpassant"
        return False
    def canpawnpromove(self):
        for i in pieceslist:
            if i != "none" and i != self:
                if i.square == self.square: return False
        return True

    #PAWN PROMOTION METHOD:
    def promote(self):
        global positionset
        if not self.which == "pawn":
            raise(TypeError)
        else:
            if i.color == "white": i.img = wpromotion
            else: i.img = bpromotion
        refreshPositions()
        positionset[-1] = position

    #CASTLING METHOD
    def castle(self, king, rook, side):
        global position, wturn, positionset
        castlesound.play()
        #WHITE IS CASTLING
        if king.color == "white":
            #CHECKING FOR BOARD ROTATION
            if rot == 1:
                #CHECKING FOR CASTLING SIDE
                if side == "kingside":
                    position = position[:-3]
                    position += "1RK1"
                elif side == "queenside":
                    count = 0
                    n = 0
                    for c in position:
                        n += 1
                        if c == "/": count += 1
                        if c == "/" and count == 7: ind = n
                    position = position[:ind] + "2KR1" + position[ind + 3:]
            #CHECKING FOR BOARD ROTATION
            elif rot == -1:
                #CHECKING FOR CASTLING SIDE
                if side == "kingside":
                    ind = position.index("/")
                    position = position[:ind-3] + "1RK2" + position[ind:]
                elif side == "queenside":
                    position = "1KR1" + position[3:]
        #BLACK IS CASTLING
        elif king.color == "black":
            #CHECKING FOR BOARD ROTATION
            if rot == 1:
                #CHECKING FOR CASTLING SIDE
                if side == "queenside":
                    position = "2kr1" + position[3:]
                elif side == "kingside":
                    ind = position.index("/")
                    position = position[:ind-3] + "1rk1" + position[ind:]
            #CHECKING FOR BOARD ROTATION
            elif rot == -1:
                #CHECKING FOR CASTLING SIDE
                if side == "kingside":
                    position = position[:-3]
                    position += "1rk2"
                elif side == "queenside":
                    count = 0
                    n = 0
                    for c in position:
                        n += 1
                        if c == "/": count += 1
                        if c == "/" and count == 7: ind = n
                    position = position[:ind] + "1kr1" + position[ind + 3:]

        defBoardPieces()
        if wturn: wturn = False
        else: wturn = True
        king.isfirstmove = False
        rook.isfirstmove = False
        positionset.append(position)

"""---------"""
"""MAIN LOOP"""
"""---------"""
startsquare = []
reset()
while True:
    clock.tick(FPS) #SETTING FPS

    """event listeners"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #EVENT: QUIT
            quit()
        
        #EVENT: MOUSE
        #-----RELEASE
        if event.type == pygame.MOUSEBUTTONUP:
            clickpos = pygame.mouse.get_pos()
            x = clickpos[0]
            y = clickpos[1]
            #print("X: " + str(x) + ", Y: " + str(y))

            #BUTTONS
            if x >= 730 and x <= 730 + BTNW and y >= 10 and y <= 10 + BTNH: #change board button
                btnboardchoice.pressed = True
                if boardnumber < len(boards) - 1: boardnumber += 1
                else: boardnumber = 0
            if x >= 730 and x <= 730 + BTNW and y >= 70 and y <= 70 + BTNH: #change style button
                btnstylechoice.pressed = True
                if stylenumber < 3: stylenumber += 1
                else: stylenumber = 1
                refreshstyle()
                defBoardPieces()
            if x >= 730 and x <= 730 + BTNW and y >= 130 and y <= 130 + BTNH: #reset button
                btnreset.pressed = True
                reset()
            if x >= 730 and x <= 730 + BTNW and y >= 190 and y <= 190 + BTNH: #rotate button
                btnrotate.pressed = True
                rotate()
            if x >= 730 and x <= 730 + BTNW/2-10 and y >= 250 and y <= 250 + BTNH: #undo button
                btnundo.pressed = True
                undo()
            if x >= 730+10+BTNW/2 and x <= 730+10+BTNW/2 + BTNW/2 - 10 and y >= 250 and y <= 250 + BTNH: #redo button
                btnredo.pressed = True
                redo()
            #WHITE PROMOTION BUTTONS
            if x >= WIDTH-165 and x <= WIDTH-145 and y >= HEIGHT-95 and y <= HEIGHT-75: #queen
                wpromotion = queens[0]
            if x >= WIDTH-140 and x <= WIDTH-120 and y >= HEIGHT-94 and y <= HEIGHT-74: #rook
                wpromotion = rooks[0]
            if x >= WIDTH-115 and x <= WIDTH-105 and y >= HEIGHT-94 and y <= HEIGHT-74: #bishop
                wpromotion = bishops[0]
            if x >= WIDTH-90 and x <= WIDTH-80 and y >= HEIGHT-94 and y <= HEIGHT-74: #knight
                wpromotion = knights[0]
            #BLACK PROMOTION BUTTONS
            if x >= WIDTH-165 and x <= WIDTH-145 and y >= HEIGHT-35 and y <= HEIGHT-15: #queen
               bpromotion = queens[1]
            if x >= WIDTH-140 and x <= WIDTH-120 and y >= HEIGHT-34 and y <= HEIGHT-14: #rook
                bpromotion = rooks[1]
            if x >= WIDTH-115 and x <= WIDTH-105 and y >= HEIGHT-34 and y <= HEIGHT-14: #bishop
                bpromotion = bishops[1]
            if x >= WIDTH-90 and x <= WIDTH-80 and y >= HEIGHT-34 and y <= HEIGHT-14: #knight
                bpromotion = knights[1]

            #DROP AFTER DRAG
            sqr = getsquare(x, y)
            for i in pieceslist:
                if not i == "none":
                    if i.dragging:
                        i.dragging = False
                        try:
                            if (pieceslist[findsquareposition(startsquare[0], startsquare[1])].color == "white" and wturn) or (pieceslist[findsquareposition(startsquare[0], startsquare[1])].color == "black" and not wturn):
                                #checks if it's the turn of the piece moved
                                if i.islegalmove(startsquare, sqr): #checks if the move is a legal one
                                    if undocount <= 1: #checks if it's analysis
                                        sq = squarepos(i.square[0], i.square[1])
                                        i.x = sq[1]
                                        i.y = sq[0]
                                        
                                        #SOUND SYSTEM
                                        wasempty = pieceslist[findsquareposition(i.square[0], i.square[1])] == "none"

                                        #PERFORMING THE MOVE INSIDE pieceslist
                                        pieceslist[findsquareposition(startsquare[0], startsquare[1])] = "none"
                                        pieceslist[findsquareposition(i.square[0], i.square[1])] = i

                                        #checks if the piece moved outside of its square
                                        if pieceslist[findsquareposition(i.square[0], i.square[1])].square != startsquare:
                                            """----------------------------------------------------------------"""
                                            """-------------------------MOVE PERFORMED-------------------------"""
                                            """----------------------------------------------------------------"""
                                            #CHECK SYSTEM
                                            for el in pieceslist:
                                                if el != "none":
                                                    ck = check(el, pieceslist)
                                                    if ck[0]: #THERE IS A CHECK
                                                        pieceslist[ck[1]].ischecked = True
                                                        checksound.play()
                                                        donesound = True
                                                        break
                                                    pieceslist[ck[1]].ischecked = False

                                            #SOUND SYSTEM
                                            if not donesound:
                                                if not wasempty:
                                                    capturesound.play()
                                                else: movesound.play()
                                            else: donesound = False
                                            
                                            #EN-PASSANT SYSTEM (for pawns)
                                            for el in pieceslist:
                                                if el != "none":
                                                    el.dmoved = False
                                            
                                            #TURN SYSTEM
                                            if wturn: wturn = False
                                            else: wturn = True

                                            #POSITION STORING SYSTEM
                                            refreshPositions()
                                            if positionset[-1] != position:
                                                if rot == 1: positionset.append(position)
                                                elif rot == -1: positionset.append(position[::-1])

                                            #PROMOTION SYSTEM
                                            if i.which == "pawn":
                                                if i.square[1] == 8 or i.square[1] == 1:
                                                    i.promote()
                                            
                                            #DOUBLE ADVANCING SYSTEM (for pawns)
                                            if i.isfirstmove:
                                                i.isfirstmove = False
                                                if i.which == "pawn":
                                                    if abs(i.square[1] - startsquare[1]) == 2:
                                                        i.dmoved = True
                                            
                                            #ADVANTAGE SYSTEM
                                            calcAdvantage()
                                            """----------------------------------------------------------------"""
                                            """----------------------------------------------------------------"""
                                            """----------------------------------------------------------------"""
                                        else: pass #PIECE MOVED ON ITS SQUARE
                                    else: raise() #TRYING TO MOVE DURING ANALYSIS
                                else: raise() #ILLEGAL MOVE
                            else: raise() #TRYING TO MOVE ON WRONG TURN
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            print(str(e) + " ERROR AT LINE " + str(exc_tb.tb_lineno))
                            
                            sq = squarepos(startsquare[0], startsquare[1])
                            i.x = sq[1]
                            i.y = sq[0]
                    
        #-----CLICK
        #----------LEFT CLICK
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            clickpos = pygame.mouse.get_pos()
            x = clickpos[0]
            y = clickpos[1]
            sqr = getsquare(x, y)
            #print("X: " + str(x) + ", Y: " + str(y))

            for i in pieceslist:
                if not i == "none":
                    if sqr == i.square:
                        startsquare = sqr
                        i.dragging = True
        #----------RIGHT CLICK
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[1]:
            pass
        
        #-----DRAG
        #----------LEFT BUTTON
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            clickpos = pygame.mouse.get_pos()
            x = clickpos[0]
            y = clickpos[1]
            sqr = getsquare(x, y)
            #print("X: " + str(x) + ", Y: " + str(y))
            
            for i in pieceslist:
                if not i == "none":
                    if i.dragging:
                        i.drag(x, y)
        #----------RIGHT BUTTON
        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[1]:
            pass

    """KEY LISTENERS"""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        quit()

    drawgame()
