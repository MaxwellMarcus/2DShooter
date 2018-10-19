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
class Character:
    def __init__(self,name,left,right,jump,file):
        self.size = root.winfo_screenwidth()/25
        self.leftInput = left
        self.rightInput = right
        self.jumpInput = jump
        self.dead = False
        self.left = False
        self.right = False
        self.aimcolor = "blue"
        self.aimcolorchange = 0
        self.speedx = root.winfo_screenwidth()/2500
        self.speedy = root.winfo_screenheight()/2500
        self.x = root.winfo_screenwidth()/2
        self.y = (root.winfo_screenheight()/100)*92 - self.size/2
        self.originaly = (root.winfo_screenheight()/100)*92 - self.size/2
        self.cursorX = self.x
        self.cursorY = self.y
        self.avatarBlue = PhotoImage(file = file)
        self.avatarBlueNewSize = int(self.avatarBlue.width()/self.size)
        self.avatarBlue = self.avatarBlue.subsample(self.avatarBlueNewSize)
        self.gunStrength = root.winfo_screenwidth()/5
        self.graphics = canvas.create_rectangle(self.x - self.size/2,self.y - self.size/2,self.x + self.size/2,self.y - self.size/2)
        self.aim = canvas.create_line(self.x,self.y,self.x,self.y)
        self.jump = False
        self.jumped = 0
        self.name = name

        root.bind("<Button-1>", self.fire,add='+')
        root.bind('<KeyPress>', self.changeMove,add='+')
        root.bind('<KeyRelease>', self.stopMove,add='+')

    def changeMove(self,event):
        if event.keysym in self.leftInput:
            self.left = True
        if event.keysym in self.rightInput:
            self.right = True
        if event.keysym in self.jumpInput:
            if self.y == self.originaly:
                self.jump = True

    def stopMove(self,event):
        if event.keysym == "a":
            self.left = False
        if event.keysym == "d":
            self.right = False

    def move(self):
        if self.left:
            if self.x > 0 + self.size/2:
                self.x -= self.speedx
        if self.right:
            if self.x < root.winfo_screenwidth() - self.size/2:
                self.x += self.speedx
        if self.jump:
            if self.y == self.originaly or self.jump:
                if self.jumped < self.size * 3:
                    self.y -= .5
                    self.jumped += .5
                else:
                    self.jump = False
                    self.jumped = 0
        if not self.y == self.originaly and not self.jump:
            self.y += .5

    def moveCursor(self):
        self.mousePosX = root.winfo_pointerx()
        self.mousePosY = root.winfo_pointery()
        if self.mousePosX < self.x + self.gunStrength and self.mousePosX > self.x - self.gunStrength:
            self.cursorX = self.mousePosX
        else:
            if self.mousePosX > self.x:
                self.cursorX = self.x + self.gunStrength
            if self.mousePosX < self.x:
                self.cursorX = self.x - self.gunStrength
        if self.mousePosY < self.y + self.gunStrength and self.mousePosY > self.y - self.gunStrength:
            self.cursorY = self.mousePosY
        else:
            if self.mousePosY > self.y:
                self.cursorY = self.y + self.gunStrength
            if self.mousePosY < self.y:
                self.cursorY = self.y - self.gunStrength
    def fire(self,event):
        i = 0
        self.aimcolor = "black"
        self.aimcolorchange = time.time()
        while i < len(objects)-1:
            objects[i].isHit(self.cursorX,self.cursorY)
            i += 1
    def isHit(self,x,y):
        if x > self.x - self.size/2 and x < self.x + self.size/2:
            print("worling")
            if y > self.y - self.size/2 and y < self.x + self.size/2:
                print("working")
                self.dead = True
                objects.remove(self.name)

    def render(self):
        canvas.delete(self.graphics)
        canvas.delete(self.aim)
        if time.time() - self.aimcolorchange > .1:
            self.aimcolor = "gray"
            self.aimcolorchange = 0
        if not self.dead:
            self.aim = canvas.create_line(self.x,self.y,self.cursorX,self.cursorY,fill = self.aimcolor,width = 10)
            self.graphics = canvas.create_image(self.x,self.y,image = self.avatarBlue)

def start(event):
    global startLoop
    startLoop = True

root.bind("<Key>",start)
root.update()
while startLoop == False:
    root.update()
    if startLoop == True:
        canvas.delete(ALL)
        character = Character(0,['a'],['d'],['w','s'],'avatarBlue.gif')
        objects.append(character)
        player = Character(1,['Left'],['Right'],['Up','Down'],'avatarRed.gif')
        objects.append(player)
        while True:
            character.moveCursor()
            character.move()
            character.render()

            player.moveCursor()
            player.move()
            player.render()
            root.update()
