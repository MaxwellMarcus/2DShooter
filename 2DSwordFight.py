try:
    from Tkinter import *
except:
    from tkinter import *

import random
import time

root = Tk()
root.config(cursor = "none")

canvas = Canvas(root,width = root.winfo_screenwidth(),height = root.winfo_screenheight(),background = "black")
canvas.pack()

canvas.create_text(root.winfo_screenwidth()/2,root.winfo_screenheight()/2 - 300,text = '''2DPvP.py''',fill = "white",font = ("TkTextFont",175))
canvas.create_text(root.winfo_screenwidth()/2,root.winfo_screenheight()/2,text = '''press left mouse to fire''',fill = "gray7",font = ("TkTextFont",25))
canvas.create_text(root.winfo_screenwidth()/2, root.winfo_screenheight()/2 + 50,text = '''move mouse to aim''',fill = "gray7",font = ("TkTextFont",25))
canvas.create_text(root.winfo_screenwidth()/2,root.winfo_screenheight()/2 + 300,text = '''Press any key to continue''',fill = "gray7",font = ("TkTextFont",75))

startLoop = False

startTime = time.time()
objects = []
class Enviroment:
    def __init__(self,sizex,sizey):
        self.grid = []
        self.sizex = sizex
        self.sizey = sizey
        self.rectSizex = (root.winfo_screenwidth()/self.sizex)
        self.rectSizey = (root.winfo_screenheight()/self.sizey)

        i = 0
        while i < sizex:
            z = 0
            self.ygrid = []
            while z < sizey:
                self.ygrid.append(0)
                z += 1
            i += 1
            self.grid.append(self.ygrid)

    def setBlock(self,x,y,on=1):
        self.grid[y-1][x-1] = on
        if startLoop:
            self.render()
    def setRow(self,x,on=1):
        i = 0
        while i < self.sizex:
            self.grid[x-1][i] = on
            i += 1
        if startLoop:
            self.render()
    def setColumn(self,y,on=1):
        i = 0
        while i < self.sizey:
            self.grid[i][y-1] = on
            i += 1
        if startLoop:
            self.render()
    def createGrid(self):
        i = 0
        while i < self.sizey:
            canvas.create_line(0,self.rectSizey*i,root.winfo_screenwidth(),self.rectSizey*i,fill = 'blue')
            i += 1
        z = 0
        while z < self.sizex:
            canvas.create_line(self.rectSizex*z,0,self.rectSizex*z,root.winfo_screenheight(),fill = 'blue')
            z += 1
    def render(self):
        canvas.delete(ALL)
        i = 0
        while i < len(self.grid):
            z = 0
            while z < len(self.grid[i]):
                if self.grid[i][z] == 1:
                    canvas.create_rectangle((z+1)*self.rectSizex,(i+1)*self.rectSizey,z*self.rectSizex,i*self.rectSizey,fill='red')
                z += 1
            i += 1
class Character:
    def __init__(self,name,left,right,jump,moveAim,gunInput,file):
        self.size = root.winfo_screenwidth()/25
        self.leftInput = left
        self.rightInput = right
        self.jumpInput = jump
        self.mouseInput = moveAim
        self.gunInput = gunInput
        self.dead = False
        self.left = False
        self.right = False
        self.mouseUp = False
        self.mouseDown = False
        self.mouseLeft = False
        self.mouseRight = False
        self.aimcolor = "blue"
        self.aimcolorchange = 0
        self.speedx = root.winfo_screenwidth()/2500
        self.speedy = root.winfo_screenheight()/2500
        self.x = root.winfo_screenwidth()/2
        self.y = (root.winfo_screenheight()/100)*92 - self.size/2
        self.originaly = (root.winfo_screenheight()/100)*92 - self.size/2
        self.cursorX = self.x
        self.cursorY = self.y
        if not 'none_' in file:
            self.file = file
            self.avatarBlue = PhotoImage(file = file)
            self.avatarBlueNewSize = int(self.avatarBlue.width()/self.size)
            self.avatarBlue = self.avatarBlue.subsample(self.avatarBlueNewSize)
        else:
            self.file = file
        self.gunStrength = root.winfo_screenwidth()/5
        self.graphics = canvas.create_rectangle(self.x - self.size/2,self.y - self.size/2,self.x + self.size/2,self.y - self.size/2)
        self.aim = canvas.create_line(self.x,self.y,self.x,self.y)
        self.jump = False
        self.jumped = 0
        self.name = name
        self.swordLengthX = self.size*2
        self.swordLengthY = -self.size/3#-root.winfo_screenheight()/30
        self.swordDirction = 1
        self.cursorSpeed = root.winfo_screenwidth()/8000
        self.jumpSpeed = root.winfo_screenheight()/1500
        self.gravSpeed = root.winfo_screenheight()/1500
        self.hit = 0
        self.stillHit = 0
        if self.gunInput == 'mouse_button':
            root.bind('<Button-1>',self.fire,add='+')
        else:
            root.bind('<KeyPress>', self.fire,add='+')
        root.bind('<KeyPress>', self.changeMove,add='+')
        root.bind('<KeyRelease>', self.stopMove,add='+')

    def changeMove(self,event):
        if event.keysym in self.leftInput:
            self.left = True
            self.swordDirction = -1
        if event.keysym in self.rightInput:
            self.right = True
            self.swordDirction = 1
        if event.keysym in self.jumpInput:
            spoty = int((self.y + self.size/2)/enviroment.rectSizey)
            spotx = int((self.x + self.size/2)/enviroment.rectSizex)
            if enviroment.grid[spoty][spotx] == 1:
                self.jump = True

    def stopMove(self,event):

        if event.keysym in self.leftInput:
            self.left = False
        if event.keysym in self.rightInput:
            self.right = False

    def move(self):
        spoty = (self.y + self.size/2)/enviroment.rectSizey
        spot_x_leftside = (self.x - self.size/2)/enviroment.rectSizex
        spot_x_rightside = (self.x + self.size/2)/enviroment.rectSizex

        if self.hit == 0:
            if self.left:
                if self.x > 0 + self.size/2:
                    self.x -= self.speedx
            if self.right:
                if self.x < root.winfo_screenwidth() - self.size/2:
                    self.x += self.speedx
        else:
            if self.stillHit <= 200:
                if self.x < root.winfo_screenwidth() - self.size/2 and self.x > 0 + self.size/2:
                    self.x += self.speedx * 2 * self.hit
                self.stillHit += 1
            else:
                self.hit = 0
        if self.jump:
            if (not enviroment.grid[int(spoty)][int(spot_x_leftside)] == 1 or not enviroment.grid[int(spoty)][int(spot_x_rightside)] == 1) or self.jump:
                if self.jumped < enviroment.rectSizey*2.75 and self.y - self.size/2 > 0:
                        self.y -= self.jumpSpeed
                        self.jumped += self.jumpSpeed
                else:
                    self.jump = False
                    self.jumped = 0

        if (not enviroment.grid[int(spoty)][int(spot_x_leftside)] == 1 or not enviroment.grid[int(spoty)][int(spot_x_rightside)] == 1) and not self.jump:
            self.y += self.gravSpeed

    def fire(self,event):
        if event.keysym in self.gunInput or self.gunInput == 'mouse_button':
            i = 0
            self.aimcolor = "black"
            self.aimcolorchange = time.time()
            while i < len(objects):
                if self.swordDirction == 1:
                    objects[i].isHit(range(int(self.x),int(self.x + self.swordLengthX*self.swordDirction)),self.y + self.size/2,self.swordDirction,self.name)
                else:
                    objects[i].isHit(range(int(self.x + self.swordLengthX*self.swordDirction),int(self.x)),self.y + self.size/2,self.swordDirction,self.name)
                i += 1
    def isHit(self,x,bottomY,direction,name):
        if not self.name == name:
            for z in range(int(self.x - self.size/2),int(self.x + self.size/2)):
                if z in x:
                    if self.y <= bottomY:
                        if direction == -1:
                            self.stillHit = 0
                            self.hit = -1
                        else:
                            self.stillHit = 0
                            self.hit = 1

    def render(self):
        canvas.delete(self.graphics)
        canvas.delete(self.aim)
        if time.time() - self.aimcolorchange > .1:
            self.aimcolor = "gray"
            self.aimcolorchange = 0
        if not self.dead:
            self.aim = canvas.create_line(self.x,self.y,self.x + self.swordLengthX*self.swordDirction,self.y + self.swordLengthY,fill = self.aimcolor,width = 6)
            if not 'none_' in self.file:
                self.graphics = canvas.create_image(self.x,self.y,image = self.avatarBlue)
            else:
                self.color = self.file.replace("none_",'')
                self.graphics = canvas.create_rectangle(self.x - self.size/2,self.y - self.size/2,self.x + self.size/2,self.y + self.size/2,fill = self.color)


def start(event):
    global startLoop
    startLoop = True

root.bind("<Key>",start)
root.update()

enviroment = Enviroment(10,10)
enviroment.setRow(10)
enviroment.setBlock(1,10,0)
enviroment.setBlock(10,10,0)
enviroment.setBlock(2,8)
enviroment.setBlock(4,6)
enviroment.setBlock(6,4)
enviroment.setBlock(8,2)
enviroment.setBlock(10,1)
while startLoop == False:
    root.update()
    if startLoop == True:
        canvas.delete(ALL)
        character = Character(0,['a'],['d'],['w','s'],['i','l','k','j'],['space'],'none_blue')
        objects.append(character)
        player = Character(1,['Left'],['Right'],['Up','Down'],'motion','mouse_button','none_red')
        objects.append(player)
        enviroment.render()

        enviroment.createGrid()
        while True:

            character.move()
            character.render()

            player.move()
            player.render()

            root.update()
