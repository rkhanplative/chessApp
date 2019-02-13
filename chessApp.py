import pygame
import time
import sys
import os
import signal
pygame.init()
pygame.font.init()

class Pawn:
    global board, cleanBoard,tileW,tileH,topX,topY,boxW,boxH
    def __init__(self, x,y,color):
        global tileW, tileH
        self.x = x
        self.y = y
        self.color = color
        self.posMoves = []
        self.posKill = []
        self.blitIcon()
    def killed(self,count):
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightPond.png"),(int(tileW*0.7*0.5),int(tileH*0.5))),(topX+boxW+70,count*(int(tileH*0.5))+topY))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkPond.png"),(int(tileW*0.8*0.5),int(tileH*0.5))),(topX+boxW+70+int(tileW*0.7*0.5),count*int(tileH*0.5)+topY))
    def __str__(self):
        return '{}'.format(self.color)
    def unselect(self,x,y):
        for locations in self.posMoves:
            if cleanBoard[locations[1]][locations[0]] == "light":
                pygame.draw.rect(screen,(244,192,149),(locations[0]*tileW+topX+10,locations[1]*tileH+topY+10,tileW,tileH))
            else:
                pygame.draw.rect(screen,(114,61,70),(locations[0]*tileW+topX+10,locations[1]*tileH+topY+10,tileW,tileH))
        for locations in self.posKill:
            if locations != [x,y]:
                board[locations[1]][locations[0]].blitIcon()
    def blitIcon(self):
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightPond.png"),(int(tileW*0.7),tileH)),(self.x*tileW+topX+35,self.y*tileH+topY+10))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkPond.png"),(int(tileW*0.8),tileH)),(self.x*tileW+topX+30,self.y*tileH+topY+10))
    def showMoves(self):
        if self.color == "light":
            if board[self.y-2][self.x] == 0 and self.y == 6:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(self.x*tileW+topX+25,(self.y-2)*tileH+topY+30))
                self.posMoves.append([self.x,self.y-2])
            if board[self.y-1][self.x] == 0 and self.y>=1:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(self.x*tileW+topX+25,(self.y-1)*tileH+topY+30))
                self.posMoves.append([self.x,self.y-1])
            if self.y>=1 and self.x >=1 and str(board[self.y-1][self.x-1])=="dark":
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x-1)*tileW+topX+25,(self.y-1)*tileH+topY+30))
                self.posMoves.append([self.x-1,self.y-1])
                self.posKill.append([self.x-1,self.y-1])
            if self.y>=1 and self.x <= 6 and str(board[self.y-1][self.x+1])=="dark":
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x+1)*tileW+topX+25,(self.y-1)*tileH+topY+30))
                self.posMoves.append([self.x+1,self.y-1])
                self.posKill.append([self.x+1,self.y-1])
        if self.color == "dark":
            if board[self.y+2][self.x] == 0 and self.y == 1:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(self.x*tileW+topX+25,(self.y+2)*tileH+topY+30))
                self.posMoves.append([self.x,self.y+2])
            if board[self.y+1][self.x] == 0 and self.y<=6:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(self.x*tileW+topX+25,(self.y+1)*tileH+topY+30))
                self.posMoves.append([self.x,self.y+1])
            if self.y<=6 and self.x >=1 and str(board[self.y+1][self.x-1])=="light":
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x-1)*tileW+topX+25,(self.y+1)*tileH+topY+30))
                self.posMoves.append([self.x-1,self.y+1])
                self.posKill.append([self.x-1,self.y+1])
            if self.y<=6 and self.x <= 6 and str(board[self.y+1][self.x+1])=="light":
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x+1)*tileW+topX+25,(self.y+1)*tileH+topY+30))
                self.posMoves.append([self.x+1,self.y+1])
                self.posKill.append([self.x+1,self.y+1])
    def selected(self):
        pygame.draw.rect(screen,(0,255,0),(self.x*tileW+topX+10,self.y*tileH+topY+10,tileW,tileH))
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightPond.png"),(int(tileW*0.7),tileH)),(self.x*tileW+topX+35,self.y*tileH+topY+10))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkPond.png"),(int(tileW*0.8),tileH)),(self.x*tileW+topX+30,self.y*tileH+topY+10))
    def moveTo(self,x,y):
        self.unselect(x,y)
        self.posMoves = []
        self.posKill = []
        board[y][x] = board[self.y][self.x]
        board[self.y][self.x] = 0
        self.x = x
        self.y = y
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightPond.png"),(int(tileW*0.7),tileH)),(self.x*tileW+topX+35,self.y*tileH+topY+10))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkPond.png"),(int(tileW*0.8),tileH)),(self.x*tileW+topX+30,self.y*tileH+topY+10))
    def canMoveTo(self,x,y):
        return [x,y] in self.posMoves
class Rook:
    global board, cleanBoard,tileW,tileH,topX,topY,boxH,boxW
    def __str__(self):
        return '{}'.format(self.color)
    def __init__(self, x,y,color):
        self.x = x
        self.y = y
        self.color = color
        self.blitIcon()
        self.posMoves = []
        self.posKill = []
    def killed(self,count):
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightRook.png"),(int(tileW*0.7*0.5),int(tileH*0.5))),(topX+boxW+70,count*(int(tileH*0.5))+topY))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkRook.png"),(int(tileW*0.8*0.5),int(tileH*0.5))),(topX+boxW+70+int(tileW*0.7*0.5),count*int(tileH*0.5)+topY))
    def blitIcon(self):
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightRook.png"),(int(tileW*0.7),tileH)),(self.x*tileW+topX+35,self.y*tileH+topY+10))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkRook.png"),(int(tileW*0.8),tileH)),(self.x*tileW+topX+30,self.y*tileH+topY+10))
    def unselect(self,x,y):
        for self.locations in self.posMoves:
            if cleanBoard[self.locations[1]][self.locations[0]] == "light":
                pygame.draw.rect(screen,(244,192,149),(self.locations[0]*tileW+topX+10,self.locations[1]*tileH+topY+10,tileW,tileH))
            else:
                pygame.draw.rect(screen,(114,61,70),(self.locations[0]*tileW+topX+10,self.locations[1]*tileH+topY+10,tileW,tileH))
        for locations in self.posKill:
            if locations != [x,y]:
                board[locations[1]][locations[0]].blitIcon()
    def canMoveTo(self,x,y):
        return [x,y] in self.posMoves
    def showMoves(self):
        curX = self.x+1
        curY = self.y
        while curX <= 7 and board[self.y][curX] == 0:
            if board[self.y][curX] != 0:
                break
            self.posMoves.append([curX,self.y])
            screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(self.y)*tileH+topY+30))
            curX+=1
        if curX <= 7 and board[self.y][curX] != 0 and str(board[self.y][curX]) != str(board[self.y][self.x]):
            screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((curX)*tileW+topX+25,(self.y)*tileH+topY+30))
            self.posMoves.append([curX,self.y])
            self.posKill.append([curX,self.y])
        curX = self.x-1
        while curX >= 0 and board[self.y][curX] == 0:
            if board[self.y][curX] != 0:
                break
            self.posMoves.append([curX,self.y])
            screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(self.y)*tileH+topY+30))
            curX-=1
        if curX >= 0 and board[self.y][curX] != 0 and str(board[self.y][curX]) != str(board[self.y][self.x]):
            screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((curX)*tileW+topX+25,(self.y)*tileH+topY+30))
            self.posMoves.append([curX,self.y])
            self.posKill.append([curX,self.y])
        curY += 1
        
        while curY <= 7:
            if board[curY][self.x] != 0:
                break
            self.posMoves.append([self.x,curY])
            screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(self.x*tileW+topX+25,(curY)*tileH+topY+30))
            curY+=1
        if curY <= 7 and board[curY][self.x] != 0 and str(board[curY][self.x]) != str(board[self.y][self.x]):
            screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x)*tileW+topX+25,(curY)*tileH+topY+30))
            self.posMoves.append([self.x,curY])
            self.posKill.append([self.x,curY])
        curY = self.y-1
        while curY >= 0:
            if board[curY][self.x] != 0:
                break
            self.posMoves.append([self.x,curY])
            screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(self.x*tileW+topX+25,(curY)*tileH+topY+30))
            curY-=1
        if curY >= 0 and board[curY][self.x] != 0 and str(board[curY][self.x]) != str(board[self.y][self.x]):
            screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x)*tileW+topX+25,(curY)*tileH+topY+30))
            self.posMoves.append([self.x,curY])
            self.posKill.append([self.x,curY])
    def selected(self):
        pygame.draw.rect(screen,(0,255,0),(self.x*tileW+topX+10,self.y*tileH+topY+10,tileW,tileH))
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightRook.png"),(int(tileW*0.7),tileH)),(self.x*tileW+topX+35,self.y*tileH+topY+10))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkRook.png"),(int(tileW*0.8),tileH)),(self.x*tileW+topX+30,self.y*tileH+topY+10))
    def moveTo(self,x,y):
        global board
        self.unselect(x,y)
        self.posMoves = []
        self.posKill = []
        board[y][x] = board[self.y][self.x]
        board[self.y][self.x] = 0
        self.x = x
        self.y = y
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightRook.png"),(int(tileW*0.7),tileH)),(self.x*tileW+topX+35,self.y*tileH+topY+10))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkRook.png"),(int(tileW*0.8),tileH)),(self.x*tileW+topX+30,self.y*tileH+topY+10))
class Knight:
    global board, cleanBoard,tileW,tileH,topX,topY,boxH,boxW
    def __str__(self):
        return '{}'.format(self.color)
    def __init__(self, x,y,color):
        self.x = x
        self.y = y
        self.color = color
        self.blitIcon()
        self.posMoves = []
        self.posKill = []
    def killed(self,count):
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightKnight.png"),(int(tileW*0.7*0.5),int(tileH*0.5))),(topX+boxW+70,count*(int(tileH*0.5))+topY))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkKnight.png"),(int(tileW*0.8*0.5),int(tileH*0.5))),(topX+boxW+70+int(tileW*0.7*0.5),count*int(tileH*0.5)+topY))
    def unselect(self,x,y):
        for self.locations in self.posMoves:
            if cleanBoard[self.locations[1]][self.locations[0]] == "light":
                pygame.draw.rect(screen,(244,192,149),(self.locations[0]*tileW+topX+10,self.locations[1]*tileH+topY+10,tileW,tileH))
            else:
                pygame.draw.rect(screen,(114,61,70),(self.locations[0]*tileW+topX+10,self.locations[1]*tileH+topY+10,tileW,tileH))
        for locations in self.posKill:
            if locations != [x,y]:
                print(locations[1])
                print(locations[0])
                board[locations[1]][locations[0]].blitIcon()
    def blitIcon(self):
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightKnight.png"),(int(tileW*0.7),tileH)),(self.x*tileW+topX+35,self.y*tileH+topY+10))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkKnight.png"),(int(tileW*0.8),tileH)),(self.x*tileW+topX+30,self.y*tileH+topY+10))
    def getPos(self):
        return [self.x,self.y]
    def showMoves(self):
        if self.x <= 5 and self.y>=1 and board[self.y-1][self.x+2] == 0:
            self.posMoves.append([self.x+2,self.y-1])
            screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x+2)*tileW+topX+25,(self.y-1)*tileH+topY+30))
        if self.x <= 5 and self.y<=6 and board[self.y+1][self.x+2] == 0:
            self.posMoves.append([self.x+2,self.y+1])
            screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x+2)*tileW+topX+25,(self.y+1)*tileH+topY+30))
        if self.x >= 2  and self.y>=1 and board[self.y-1][self.x-2] == 0:
            self.posMoves.append([self.x-2,self.y-1])
            screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x-2)*tileW+topX+25,(self.y-1)*tileH+topY+30))
        if self.x >= 2 and self.y<=6 and board[self.y+1][self.x-2] == 0:
            self.posMoves.append([self.x-2,self.y+1])
            screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x-2)*tileW+topX+25,(self.y+1)*tileH+topY+30))

        if self.y <= 5 and self.x>=1 and board[self.y+2][self.x-1] == 0:
            self.posMoves.append([self.x-1,self.y+2])
            screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x-1)*tileW+topX+25,(self.y+2)*tileH+topY+30))
        if self.y <= 5 and self.x<=6 and board[self.y+2][self.x+1] == 0:
            self.posMoves.append([self.x+1,self.y+2])
            screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x+1)*tileW+topX+25,(self.y+2)*tileH+topY+30))
        if self.y >= 2  and self.x>=1 and board[self.y-2][self.x-1] == 0:
            self.posMoves.append([self.x-1,self.y-2])
            screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x-1)*tileW+topX+25,(self.y-2)*tileH+topY+30))
        if self.y >= 2 and self.x<=6 and board[self.y-2][self.x+1] == 0:
            self.posMoves.append([self.x+1,self.y-2])
            screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x+1)*tileW+topX+25,(self.y+-2)*tileH+topY+30))
        
        if self.x <= 5 and self.y>=1 and str(board[self.y-1][self.x+2]) != str(board[self.y][self.x]) and board[self.y-1][self.x+2] != 0:
            self.posMoves.append([self.x+2,self.y-1])
            self.posKill.append([self.x+2,self.y-1])
            screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x+2)*tileW+topX+25,(self.y-1)*tileH+topY+30))
        if self.x <= 5 and self.y<=6 and str(board[self.y+1][self.x+2]) != str(board[self.y][self.x]) and board[self.y+1][self.x+2] != 0:
            self.posMoves.append([self.x+2,self.y+1])
            self.posKill.append([self.x+2,self.y+1])
            screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x+2)*tileW+topX+25,(self.y+1)*tileH+topY+30))
        if self.x >= 2  and self.y>=1 and str(board[self.y-1][self.x-2]) != str(board[self.y][self.x]) and board[self.y-1][self.x-2] != 0:
            self.posMoves.append([self.x-2,self.y-1])
            self.posKill.append([self.x-2,self.y-1])
            screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x-2)*tileW+topX+25,(self.y-1)*tileH+topY+30))
        if self.x >= 2 and self.y<=6 and str(board[self.y+1][self.x-2]) != str(board[self.y][self.x]) and board[self.y+1][self.x-2] != 0:
            self.posMoves.append([self.x-2,self.y+1])
            screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x-2)*tileW+topX+25,(self.y+1)*tileH+topY+30))
            self.posKill.append([self.x-2,self.y+1])
        
        if self.y <= 5 and self.x>=1 and str(board[self.y+2][self.x-1]) != str(board[self.y][self.x]) and board[self.y+2][self.x-1] != 0:
            self.posMoves.append([self.x-1,self.y+2])
            self.posKill.append([self.x-1,self.y+2])
            screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x-1)*tileW+topX+25,(self.y+2)*tileH+topY+30))
        if self.y <= 5 and self.x<=6 and str(board[self.y+2][self.x+1]) != str(board[self.y][self.x]) and board[self.y+2][self.x+1] != 0:
            self.posMoves.append([self.x+1,self.y+2])
            self.posKill.append([self.x+1,self.y+2])
            screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x+1)*tileW+topX+25,(self.y+2)*tileH+topY+30))
        if self.y >= 2  and self.x>=1 and str(board[self.y-2][self.x-1]) != str(board[self.y][self.x]) and board[self.y-2][self.x-1] != 0:
            self.posMoves.append([self.x-1,self.y-2])
            self.posKill.append([self.x-1,self.y-2])
            screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x-1)*tileW+topX+25,(self.y-2)*tileH+topY+30))
        if self.y >= 2 and self.x<=6 and str(board[self.y-2][self.x+1]) != str(board[self.y][self.x]) and board[self.y-2][self.x+1] != 0:
            self.posMoves.append([self.x+1,self.y-2])
            self.posKill.append([self.x+1,self.y-2])
            screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x+1)*tileW+topX+25,(self.y+-2)*tileH+topY+30))
    def selected(self):
        pygame.draw.rect(screen,(0,255,0),(self.x*tileW+topX+10,self.y*tileH+topY+10,tileW,tileH))
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightKnight.png"),(int(tileW*0.7),tileH)),(self.x*tileW+topX+35,self.y*tileH+topY+10))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkKnight.png"),(int(tileW*0.8),tileH)),(self.x*tileW+topX+30,self.y*tileH+topY+10))
    def moveTo(self,x,y):
        global board
        self.unselect(x,y)
        self.posMoves = []
        self.posKill = []
        board[y][x] = board[self.y][self.x]
        board[self.y][self.x] = 0
        self.x = x
        self.y = y
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightKnight.png"),(int(tileW*0.7),tileH)),(self.x*tileW+topX+35,self.y*tileH+topY+10))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkKnight.png"),(int(tileW*0.8),tileH)),(self.x*tileW+topX+30,self.y*tileH+topY+10))
    def canMoveTo(self,x,y):
        return [x,y] in self.posMoves
class King:
    global board, cleanBoard,tileW,tileH,topX,topY,boxW,boxH
    def __str__(self):
        return '{}'.format(self.color)
    def __init__(self, x,y,color):
        self.x = x
        self.y = y
        self.color = color
        self.posMoves = []
        self.posKill = []
        self.blitIcon()
    def killed(self,count):
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightKing.png"),(int(tileW*0.7*0.5),int(tileH*0.5))),(topX+boxW+70,count*(int(tileH*0.5))+topY))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkKing.png"),(int(tileW*0.8*0.5),int(tileH*0.5))),(topX+boxW+70+int(tileW*0.7*0.5),count*int(tileH*0.5)+topY))
    def blitIcon(self):
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightKing.png"),(int(tileW*0.7),tileH)),(self.x*tileW+topX+35,self.y*tileH+topY+10))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkKing.png"),(int(tileW*0.8),tileH)),(self.x*tileW+topX+30,self.y*tileH+topY+10))
    def unselect(self,x,y):
        for self.locations in self.posMoves:
            if cleanBoard[self.locations[1]][self.locations[0]] == "light":
                pygame.draw.rect(screen,(244,192,149),(self.locations[0]*tileW+topX+10,self.locations[1]*tileH+topY+10,tileW,tileH))
            else:
                pygame.draw.rect(screen,(114,61,70),(self.locations[0]*tileW+topX+10,self.locations[1]*tileH+topY+10,tileW,tileH))
        for locations in self.posKill:
            if locations != [x,y]:
                board[locations[1]][locations[0]].blitIcon()
    def canMoveTo(self,x,y):
        return [x,y] in self.posMoves
    def showMoves(self):
        if self.y<=6 and board[self.y+1][self.x] == 0:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(self.x*tileW+topX+25,(self.y+1)*tileH+topY+30))
                self.posMoves.append([self.x,self.y+1])
        if self.x<=6 and board[self.y][self.x+1] == 0:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x+1)*tileW+topX+25,(self.y)*tileH+topY+30))
                self.posMoves.append([self.x+1,self.y])
        if self.y>=1 and board[self.y-1][self.x] == 0:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(self.x*tileW+topX+25,(self.y-1)*tileH+topY+30))
                self.posMoves.append([self.x,self.y-1])
        if self.x>=1 and board[self.y][self.x-1] == 0:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x-1)*tileW+topX+25,(self.y)*tileH+topY+30))
                self.posMoves.append([self.x-1,self.y])
        if self.x>=1 and self.y>=1 and board[self.y-1][self.x-1] == 0:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x-1)*tileW+topX+25,(self.y-1)*tileH+topY+30))
                self.posMoves.append([self.x-1,self.y-1])
        if self.x<=6 and self.y>=1 and board[self.y-1][self.x+1] == 0:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x+1)*tileW+topX+25,(self.y-1)*tileH+topY+30))
                self.posMoves.append([self.x+1,self.y-1])
        if self.y<=6 and self.x>=1 and board[self.y+1][self.x-1] == 0:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x-1)*tileW+topX+25,(self.y+1)*tileH+topY+30))
                self.posMoves.append([self.x-1,self.y+1])
        if self.x<=6 and self.y<=6 and board[self.y+1][self.x+1] == 0:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x+1)*tileW+topX+25,(self.y+1)*tileH+topY+30))
                self.posMoves.append([self.x+1,self.y+1])
        
        if self.y<=6 and board[self.y+1][self.x] != 0 and str(board[self.y+1][self.x]) != str(board[self.y][self.x]):
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),(self.x*tileW+topX+25,(self.y+1)*tileH+topY+30))
                self.posMoves.append([self.x,self.y+1])
                self.posKill.append([self.x,self.y+1])
        if self.x<=6 and board[self.y][self.x+1] != 0 and str(board[self.y][self.x+1]) != str(board[self.y][self.x]):
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x+1)*tileW+topX+25,(self.y)*tileH+topY+30))
                self.posMoves.append([self.x+1,self.y])
                self.posKill.append([self.x+1,self.y])
        if self.y>=1 and board[self.y-1][self.x] != 0 and str(board[self.y-1][self.x]) != str(board[self.y][self.x]):
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),(self.x*tileW+topX+25,(self.y-1)*tileH+topY+30))
                self.posMoves.append([self.x,self.y-1])
                self.posKill.append([self.x,self.y-1])
        if self.x>=1 and board[self.y][self.x-1] != 0 and str(board[self.y][self.x-1]) != str(board[self.y][self.x]):
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x-1)*tileW+topX+25,(self.y)*tileH+topY+30))
                self.posMoves.append([self.x-1,self.y])
                self.posKill.append([self.x-1,self.y])
        if self.x>=1 and self.y>=1 and board[self.y-1][self.x-1] != 0 and str(board[self.y-1][self.x-1]) != str(board[self.y][self.x]):
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x-1)*tileW+topX+25,(self.y-1)*tileH+topY+30))
                self.posMoves.append([self.x-1,self.y-1])
                self.posKill.append([self.x-1,self.y-1])
        if self.x<=6 and self.y>=1 and board[self.y-1][self.x+1] != 0 and str(board[self.y-1][self.x+1]) != str(board[self.y][self.x]):
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x+1)*tileW+topX+25,(self.y-1)*tileH+topY+30))
                self.posMoves.append([self.x+1,self.y-1])
                self.posKill.append([self.x+1,self.y-1])
        if self.y<=6 and self.x>=1 and board[self.y+1][self.x-1] != 0 and str(board[self.y+1][self.x-1]) != str(board[self.y][self.x]):
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x-1)*tileW+topX+25,(self.y+1)*tileH+topY+30))
                self.posMoves.append([self.x-1,self.y+1])
                self.posKill.append([self.x-1,self.y+1])
        if self.x<=6 and self.y<=6 and board[self.y+1][self.x+1] != 0 and str(board[self.y+1][self.x+1]) != str(board[self.y][self.x]):
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x+1)*tileW+topX+25,(self.y+1)*tileH+topY+30))
                self.posMoves.append([self.x+1,self.y+1])
                self.posKill.append([self.x+1,self.y+1])
    def getPos(self):
        return [self.x,self.y]
    def selected(self):
        pygame.draw.rect(screen,(0,255,0),(self.x*tileW+topX+10,self.y*tileH+topY+10,tileW,tileH))
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightKing.png"),(int(tileW*0.7),tileH)),(self.x*tileW+topX+35,self.y*tileH+topY+10))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkKing.png"),(int(tileW*0.8),tileH)),(self.x*tileW+topX+30,self.y*tileH+topY+10))
    def moveTo(self,x,y):
        global board
        self.unselect(x,y)
        self.posMoves = []
        self.posKill = []
        board[y][x] = board[self.y][self.x]
        board[self.y][self.x] = 0
        self.x = x
        self.y = y
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightKing.png"),(int(tileW*0.7),tileH)),(self.x*tileW+topX+35,self.y*tileH+topY+10))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkKing.png"),(int(tileW*0.8),tileH)),(self.x*tileW+topX+30,self.y*tileH+topY+10))
class Queen:
    global board, cleanBoard,tileW,tileH,topX,topY,boxH,boxW
    def __str__(self):
        return '{}'.format(self.color)
    def __init__(self, x,y,color):
        self.posMoves = []
        self.posKill = []
        self.x = x
        self.y = y
        self.color = color
        self.blitIcon()
    def killed(self,count):
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightQueen.png"),(int(tileW*0.7*0.5),int(tileH*0.5))),(topX+boxW+70,count*(int(tileH*0.5))+topY))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkQueen.png"),(int(tileW*0.8*0.5),int(tileH*0.5))),(topX+boxW+70+int(tileW*0.7*0.5),count*int(tileH*0.5)+topY))
    def blitIcon(self):
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightQueen.png"),(int(tileW*0.7),tileH)),(self.x*tileW+topX+35,self.y*tileH+topY+10))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkQueen.png"),(int(tileW*0.8),tileH)),(self.x*tileW+topX+30,self.y*tileH+topY+10))
    def getPos(self):
        return [self.x,self.y]
    #def showMoves():
    def canMoveTo(self,x,y):
        return [x,y] in self.posMoves
    def unselect(self,x,y):
        for self.locations in self.posMoves:
            if cleanBoard[self.locations[1]][self.locations[0]] == "light":
                pygame.draw.rect(screen,(244,192,149),(self.locations[0]*tileW+topX+10,self.locations[1]*tileH+topY+10,tileW,tileH))
            else:
                pygame.draw.rect(screen,(114,61,70),(self.locations[0]*tileW+topX+10,self.locations[1]*tileH+topY+10,tileW,tileH))
        for locations in self.posKill:
            if locations != [x,y]:
                board[locations[1]][locations[0]].blitIcon()
    def showMoves(self):
        curX = self.x - 1
        curY = self.y - 1
        if self.x>=1 and self.y>=1:
            while curY>=0 and curX>=0 and board[curY][curX] == 0:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(curY)*tileH+topY+30))
                self.posMoves.append([curX,curY])
                curX-=1
                curY-=1
            if curY>=0 and curX >= 0 and str(board[curY][curX]) != str(board[self.y][self.x]):
                self.posMoves.append([curX,curY])
                self.posKill.append([curX,curY])
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(curY)*tileH+topY+30))
        curX = self.x + 1
        curY = self.y - 1
        if self.y >= 1 and self.x <= 6:
            while curX<=7 and curY >=0 and board[curY][curX] == 0:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(curY)*tileH+topY+30))
                self.posMoves.append([curX,curY])
                curX+=1
                curY-=1
            if curY>=0 and curX <= 7 and str(board[curY][curX]) != str(board[self.y][self.x]):
                self.posMoves.append([curX,curY])
                self.posKill.append([curX,curY])
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(curY)*tileH+topY+30))
        curX = self.x+1
        curY = self.y+1
        if self.x <= 6 and self.y <= 6:
            while curX <= 7 and curY <= 7 and board[curY][curX] == 0:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(curY)*tileH+topY+30))
                self.posMoves.append([curX,curY])
                curX+=1
                curY+=1
            if curY<=7 and curX <= 7 and str(board[curY][curX]) != str(board[self.y][self.x]):
                self.posMoves.append([curX,curY])
                self.posKill.append([curX,curY])
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(curY)*tileH+topY+30))
        curX = self.x-1
        curY = self.y+1
        if self.x >= 1 and self.y <= 6:
            while curX >= 0 and curY <= 7 and board[curY][curX] == 0:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(curY)*tileH+topY+30))
                self.posMoves.append([curX,curY])
                curX-=1
                curY+=1
            if curY<=7 and curX >= 0 and str(board[curY][curX]) != str(board[self.y][self.x]):
                self.posMoves.append([curX,curY])
                self.posKill.append([curX,curY])
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(curY)*tileH+topY+30))
        curX = self.x+1
        curY = self.y
        while curX <= 7 and board[self.y][curX] == 0:
            if board[self.y][curX] != 0:
                break
            self.posMoves.append([curX,self.y])
            screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(self.y)*tileH+topY+30))
            curX+=1
        if curX <= 7 and board[self.y][curX] != 0 and str(board[self.y][curX]) != str(board[self.y][self.x]):
            screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((curX)*tileW+topX+25,(self.y)*tileH+topY+30))
            self.posMoves.append([curX,self.y])
            self.posKill.append([curX,self.y])
        curX = self.x-1
        
        while curX >= 0 and board[self.y][curX] == 0:
            if board[self.y][curX] != 0:
                break
            self.posMoves.append([curX,self.y])
            screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(self.y)*tileH+topY+30))
            curX-=1
        curY += 1
        if curX >= 0 and board[self.y][curX] != 0 and str(board[self.y][curX]) != str(board[self.y][self.x]):
            screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((curX)*tileW+topX+25,(self.y)*tileH+topY+30))
            self.posMoves.append([curX,self.y])
            self.posKill.append([curX,self.y])
        while curY <= 7:
            if board[curY][self.x] != 0:
                break
            self.posMoves.append([self.x,curY])
            screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(self.x*tileW+topX+25,(curY)*tileH+topY+30))
            curY+=1
        if curY <= 7 and board[curY][self.x] != 0 and str(board[curY][self.x]) != str(board[self.y][self.x]):
            screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x)*tileW+topX+25,(curY)*tileH+topY+30))
            self.posMoves.append([self.x,curY])
            self.posKill.append([self.x,curY])
        curY = self.y-1
        while curY >= 0:
            if board[curY][self.x] != 0:
                break
            self.posMoves.append([self.x,curY])
            screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(self.x*tileW+topX+25,(curY)*tileH+topY+30))
            curY-=1
        if curY >= 0 and board[curY][self.x] != 0 and str(board[curY][self.x]) != str(board[self.y][self.x]):
            screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),((self.x)*tileW+topX+25,(curY)*tileH+topY+30))
            self.posMoves.append([self.x,curY])
            self.posKill.append([self.x,curY])
    def selected(self):
        pygame.draw.rect(screen,(0,255,0),(self.x*tileW+topX+10,self.y*tileH+topY+10,tileW,tileH))
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightQueen.png"),(int(tileW*0.7),tileH)),(self.x*tileW+topX+35,self.y*tileH+topY+10))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkQueen.png"),(int(tileW*0.8),tileH)),(self.x*tileW+topX+30,self.y*tileH+topY+10))
    def moveTo(self,x,y):
        global board
        self.unselect(x,y)
        self.posMoves = []
        self.posKill = []
        board[y][x] = board[self.y][self.x]
        board[self.y][self.x] = 0
        self.x = x
        self.y = y
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightQueen.png"),(int(tileW*0.7),tileH)),(self.x*tileW+topX+35,self.y*tileH+topY+10))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkQueen.png"),(int(tileW*0.8),tileH)),(self.x*tileW+topX+30,self.y*tileH+topY+10))
class Bishop:
    global board, cleanBoard,tileW,tileH,topX,topY,boxH,boxW
    def __str__(self):
        return '{}'.format(self.color)
    def __init__(self, x,y,color):
        self.x = x
        self.y = y
        self.color = color
        self.blitIcon()
        self.posMoves = []
        self.posKill = []
    def killed(self,count):
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightBishop.png"),(int(tileW*0.7*0.5),int(tileH*0.5))),(topX+boxW+70,count*(int(tileH*0.5))+topY))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkBishop.png"),(int(tileW*0.8*0.5),int(tileH*0.5))),(topX+boxW+70+int(tileW*0.7*0.5),count*int(tileH*0.5)+topY))
    def blitIcon(self):
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightBishop.png"),(int(tileW*0.7),tileH)),(self.x*tileW+topX+35,self.y*tileH+topY+10))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkBishop.png"),(int(tileW*0.8),tileH)),(self.x*tileW+topX+30,self.y*tileH+topY+10))
    def getPos(self):
        return [self.x,self.y]
    def showMoves(self):
        curX = self.x - 1
        curY = self.y - 1
        if self.x>=1 and self.y>=1:
            while curY>=0 and curX>=0 and board[curY][curX] == 0:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(curY)*tileH+topY+30))
                self.posMoves.append([curX,curY])
                curX-=1
                curY-=1
            if curY>=0 and curX >= 0 and str(board[curY][curX]) != str(board[self.y][self.x]):
                self.posMoves.append([curX,curY])
                self.posKill.append([curX,curY])
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(curY)*tileH+topY+30))
        curX = self.x + 1
        curY = self.y - 1
        if self.y >= 1 and self.x <= 6:
            while curX<=7 and curY >=0 and board[curY][curX] == 0:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(curY)*tileH+topY+30))
                self.posMoves.append([curX,curY])
                curX+=1
                curY-=1
            if curY>=0 and curX <= 7 and str(board[curY][curX]) != str(board[self.y][self.x]):
                self.posMoves.append([curX,curY])
                self.posKill.append([curX,curY])
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(curY)*tileH+topY+30))
        curX = self.x+1
        curY = self.y+1
        if self.x <= 6 and self.y <= 6:
            while curX <= 7 and curY <= 7 and board[curY][curX] == 0:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(curY)*tileH+topY+30))
                self.posMoves.append([curX,curY])
                curX+=1
                curY+=1
            if curY<=7 and curX <= 7 and str(board[curY][curX]) != str(board[self.y][self.x]):
                self.posMoves.append([curX,curY])
                self.posKill.append([curX,curY])
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(curY)*tileH+topY+30))
        curX = self.x-1
        curY = self.y+1
        if self.x >= 1 and self.y <= 6:
            while curX >= 0 and curY <= 7 and board[curY][curX] == 0:
                screen.blit(pygame.transform.scale(pygame.image.load("moveIndicator.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(curY)*tileH+topY+30))
                self.posMoves.append([curX,curY])
                curX-=1
                curY+=1
            if curY<=7 and curX >= 0 and str(board[curY][curX]) != str(board[self.y][self.x]):
                self.posMoves.append([curX,curY])
                self.posKill.append([curX,curY])
                screen.blit(pygame.transform.scale(pygame.image.load("kill.png"),(int(tileW*0.8),int(0.8*tileH))),(curX*tileW+topX+25,(curY)*tileH+topY+30))

    def canMoveTo(self,x,y):
        return [x,y] in self.posMoves
    def unselect(self,x,y):
        for self.locations in self.posMoves:
            if cleanBoard[self.locations[1]][self.locations[0]] == "light":
                pygame.draw.rect(screen,(244,192,149),(self.locations[0]*tileW+topX+10,self.locations[1]*tileH+topY+10,tileW,tileH))
            else:
                pygame.draw.rect(screen,(114,61,70),(self.locations[0]*tileW+topX+10,self.locations[1]*tileH+topY+10,tileW,tileH))
        for locations in self.posKill:
            if locations != [x,y]:
                print("test")
                board[locations[1]][locations[0]].blitIcon()
    def selected(self):
        pygame.draw.rect(screen,(0,255,0),(self.x*tileW+topX+10,self.y*tileH+topY+10,tileW,tileH))
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightBishop.png"),(int(tileW*0.7),tileH)),(self.x*tileW+topX+35,self.y*tileH+topY+10))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkBishop.png"),(int(tileW*0.8),tileH)),(self.x*tileW+topX+30,self.y*tileH+topY+10))
    def moveTo(self,x,y):
        global board
        self.unselect(x,y)
        self.posMoves = []
        self.posKill = []
        board[y][x] = board[self.y][self.x]
        board[self.y][self.x] = 0
        self.x = x
        self.y = y
        if self.color == "light":
            screen.blit(pygame.transform.scale(pygame.image.load("lightBishop.png"),(int(tileW*0.7),tileH)),(self.x*tileW+topX+35,self.y*tileH+topY+10))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("darkBishop.png"),(int(tileW*0.8),tileH)),(self.x*tileW+topX+30,self.y*tileH+topY+10))
def screenSetup():
    global infoObject, boxH, boxW, topX, topY, cleanBoard,tileH,tileW,screen
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    pygame.display.set_caption('Chess App')
    pygame.display.update()
    boxH = int((infoObject.current_h)*0.8)
    boxW = boxH
    topX = int(infoObject.current_w*0.5) - int(boxW/2)
    topY = int(infoObject.current_h*0.5) - int(boxH/2)
    pygame.draw.rect(screen, (244,192,149), (topX,topY,boxW,boxH))
    pygame.draw.rect(screen, ((71,45,48)), (topX,topY,boxW,boxH), 20)
    tileW = int((boxW-10)/8)
    tileH = int((boxH-10)/8)
    cleanBoard = [["light" for x in range (0,8)] for x in range(0,8)]
    print("screenSetup")
def setup():
    global board,dark,light,startTime,Game,screen,infoObject,player,Lcount,Dcount
    Lcount = 0
    Dcount = 0
    player = True
    screen.fill((226,109,92))
    screen.blit(pygame.transform.scale(pygame.image.load("refresh.png"),(100,100)),(infoObject.current_w-130,30))
    startTime = time.time()
    pygame.draw.rect(screen, (244,192,149), (topX,topY,boxW,boxH))
    pygame.draw.rect(screen, ((71,45,48)), (topX,topY,boxW,boxH), 20)
    for i in range(topX+10+tileW,topX+boxW,tileW*2):
        for k in range(topY+10,topY+boxH-tileH,tileH*2):
            pygame.draw.rect(screen, (114,61,70), (i,k,tileW,tileH))
            cleanBoard[int((k-topY)/tileH)][int((i-topX)/tileW)] = "dark"
    for i in range(topX+10,topX+boxW-tileW,tileW*2):
        for k in range(topY+10+tileH,topY+boxH,tileH*2):
            pygame.draw.rect(screen, (114,61,70), (i,k,tileW,tileH))
            cleanBoard[int((k-topY)/tileH)][int((i-topX)/tileW)] = "dark"
    dark = []
    light = []
    dark.append(Rook(0,0,"dark"))
    dark.append(Knight(1,0,"dark"))
    dark.append(Bishop(2,0,"dark"))
    dark.append(Queen(3,0,"dark"))
    dark.append(King(4,0,"dark"))
    dark.append(Bishop(5,0,"dark"))
    dark.append(Knight(6,0,"dark"))
    dark.append(Rook(7,0,"dark"))
    for i in range(0,8): 
        dark.append(Pawn(i,1,"dark"))
    for i in range(0,8): 
        light.append(Pawn(i,6,"light"))
    light.append(Rook(0,7,"light"))
    light.append(Knight(1,7,"light"))
    light.append(Bishop(2,7,"light"))
    light.append(Queen(3,7,"light"))
    light.append(King(4,7,"light"))
    light.append(Bishop(5,7,"light"))
    light.append(Knight(6,7,"light"))
    light.append(Rook(7,7,"light"))
    pygame.display.update()
    board = [dark[0:8],dark[8:16],[0]*8,[0]*8,[0]*8,[0]*8,light[0:8],light[8:16]]
    pygame.display.update()
    print("setup")
def run():
    global infoObject, tileW,topX,tileH,topY,screen,Game,player,Lcount,Dcount
    clicked = False
    running = True
    teal = (7,136,155)
    powder = (102,185,191)
    myFont1 = pygame.font.SysFont("Laksaman",int(tileH*0.8))
    myFont2 = pygame.font.SysFont("Laksaman",int(tileH*0.5))
    player = True
    killed = [[],[]]
    Lcount = 0
    Dcount = 0
    try:
        while running:
            print("running")
            pygame.draw.rect(screen,teal,(int(topX/2)-tileW,tileH*2,tileW*2,tileH),20)
            pygame.draw.rect(screen,powder,(int(topX/2)-tileW,tileH*2,tileW*2,tileH))
            pygame.draw.rect(screen,teal,(int(topX/2)-tileW,tileH*4,tileW*2,tileH),20)
            pygame.draw.rect(screen,powder,(int(topX/2)-tileW,tileH*4,tileW*2,tileH))
            current = int(time.time()-startTime)
            minutes = int(current/60)
            seconds = current-60*minutes
            outputString = "%002s:%002s"%(minutes,seconds)
            screen.blit(myFont1.render(outputString,False,teal),(int(topX/2)-tileW,tileH*1.8))
            if player:
                screen.blit(myFont2.render("Player 1",False,teal),(int(topX/2)-tileW+10,tileH*3.9))
            else:
                screen.blit(myFont2.render("Player 2",False,teal),(int(topX/2)-tileW+10,tileH*3.9))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = not(clicked)
                    pos = pygame.mouse.get_pos()
                    if (pos[0] >= infoObject.current_w-130) and (pos[0]<=infoObject.current_w-30) and (pos[1]>=30) and (pos[1]<=130):
                        setup()
                        continue
                    if clicked:
                        Olocation = pygame.mouse.get_pos()
                        oldX = int((Olocation[0] - topX)/tileW)
                        oldY = int((Olocation[1] - topY)/tileH)
                        try:
                            if (player and str(board[oldY][oldX]) == "light") or (not(player) and str(board[oldY][oldX])=="dark"):
                                if board[oldY][oldX] == 0: 
                                    clicked = False
                                    continue
                                board[oldY][oldX].selected()
                                board[oldY][oldX].showMoves()
                            else:
                                clicked = False
                                continue
                        except:
                            continue
                    else:
                        Nlocation = pygame.mouse.get_pos()
                        newX = int((Nlocation[0] - topX)/tileW)
                        newY = int((Nlocation[1] - topY)/tileH)
                        try:
                            if str(board[oldY][oldX]) == str(board[newY][newX]):
                                clicked = False
                                if cleanBoard[oldY][oldX] == "light":
                                    pygame.draw.rect(screen,(244,192,149),(oldX*tileW+topX+10,oldY*tileH+topY+10,tileW,tileH))
                                else:
                                    pygame.draw.rect(screen,(114,61,70),(oldX*tileW+topX+10,oldY*tileH+topY+10,tileW,tileH))
                                board[oldY][oldX].blitIcon()
                                board[oldY][oldX].showMoves()
                                board[oldY][oldX].unselect(newX,newY)
                                continue
                        except:
                            continue
                        try:
                            
                            if board[oldY][oldX].canMoveTo(newX,newY): 
                                if board[newY][newX] != 0:
                                    if str(board[newY][newX]) == "light":
                                        board[newY][newX].killed(Lcount)
                                        killed[0].append(board[newY][newX])
                                        Lcount+=1
                                    else:
                                        board[newY][newX].killed(Dcount)
                                        killed[1].append(board[newY][newX])
                                        Dcount+=1
                                board[oldY][oldX].moveTo(newX,newY)
                                player = not(player)
                                if cleanBoard[oldY][oldX] == "light":
                                    pygame.draw.rect(screen,(244,192,149),(oldX*tileW+topX+10,oldY*tileH+topY+10,tileW,tileH))
                                else:
                                    pygame.draw.rect(screen,(114,61,70),(oldX*tileW+topX+10,oldY*tileH+topY+10,tileW,tileH))
                        except:
                            continue
            pygame.display.update()
        pygame.display.quit()
        os.kill(os.getppid(), signal.SIGHUP)
    except SystemExit:
        pygame.quit()
screenSetup()    
setup()
run()
