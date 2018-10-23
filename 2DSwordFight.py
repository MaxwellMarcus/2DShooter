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
        self.speedx = root.winfo_screenwidth()/250
        self.speedy = root.winfo_screenheight()/250
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
        self.jumpSpeed = root.winfo_screenheight()/100
        self.gravSpeed = root.winfo_screenheight()/100
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
            if self.y == self.originaly:
                self.jump = True
        if not self.mouseInput == 'motion':
            if event.keysym == self.mouseInput[0]:
                self.mouseUp = True
            if event.keysym == self.mouseInput[1]:
                self.mouseRight = True
            if event.keysym == self.mouseInput[2]:
                self.mouseDown = True
            if event.keysym == self.mouseInput[3]:
                self.mouseLeft = True

    def stopMove(self,event):

        if event.keysym in self.leftInput:
            self.left = False
        if event.keysym in self.rightInput:
            self.right = False
        if not self.mouseInput == 'motion':
            if event.keysym == self.mouseInput[0]:
                self.mouseUp = False
            if event.keysym == self.mouseInput[1]:
                self.mouseRight = False
            if event.keysym == self.mouseInput[2]:
                self.mouseDown = False
            if event.keysym == self.mouseInput[3]:
                self.mouseLeft = False

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
                    self.y -= self.jumpSpeed
                    self.jumped += self.jumpSpeed
                else:
                    self.jump = False
                    self.jumped = 0
        if not self.y >= self.originaly and not self.jump:
            self.y += self.gravSpeed
    def moveCursor(self):
        if self.mouseInput == 'motion':
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
        else:
            if self.mouseUp and self.cursorY - 1 < self.y + self.gunStrength and self.cursorY - 1 > self.y - self.gunStrength:
                self.cursorY -= self.cursorSpeed
            if self.mouseRight and self.cursorX + 1< self.x + self.gunStrength and self.cursorX + 1 > self.x - self.gunStrength:
                self.cursorX += self.cursorSpeed
            if self.mouseDown and self.cursorY + 1< self.y + self.gunStrength and self.cursorY + 1 > self.y - self.gunStrength:
                self.cursorY += self.cursorSpeed
            if self.mouseLeft and self.cursorX - 1< self.x + self.gunStrength and self.cursorX - 1 > self.x - self.gunStrength:
                self.cursorX -= self.cursorSpeed
            if not self.cursorY < self.y + self.gunStrength:
                self.cursorY = self.y + self.gunStrength - 1
            if not self.cursorY > self.y - self.gunStrength:
                self.cursorY = self.y - self.gunStrength + 1
            if not self.cursorX < self.x + self.gunStrength:
                self.cursorX = self.x + self.gunStrength - 1
            if not self.cursorX > self.x - self.gunStrength:
                self.cursorX = self.x - self.gunStrength + 1
    def fire(self,event):
        if event.keysym in self.gunInput or self.gunInput == 'mouse_button':
            i = 0
            self.aimcolor = "black"
            self.aimcolorchange = time.time()
            while i < len(objects):
                objects[i].isHit(range(self.x,self.x + self.swordLengthX*self.swordDirction),self.y + self.size/2,self.name)
                i += 1
    def isHit(self,x,bottomY,name):
        if not self.name == name:
            for z in range(self.x - self.size/2,self.x + self.size/2):
                if z in x:
                    print('worling')
                    if self.y <= bottomY:
                        self.dead = True
                        objects.remove(objects[self.name])
        '''
        if x > self.x - self.size/2 and x < self.x + self.size/2:
            if y > self.y - self.size/2 and y < self.y + self.size/2:
                self.dead = True
                objects.remove(objects[self.name])
'''
    def render(self):
        canvas.delete(self.graphics)
        canvas.delete(self.aim)
        if time.time() - self.aimcolorchange > .1:
            self.aimcolor = "gray"
            self.aimcolorchange = 0
        if not self.dead:
            self.aim = canvas.create_line(self.x,self.y,self.x + self.swordLengthX*self.swordDirction,self.y + self.swordLengthY,fill = self.aimcolor,width = 1)
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
while startLoop == False:
    root.update()
    if startLoop == True:
        canvas.delete(ALL)
        character = Character(0,['a'],['d'],['w','s'],['i','l','k','j'],['space'],'none_blue')
        objects.append(character)
        player = Character(1,['Left'],['Right'],['Up','Down'],'motion','mouse_button','none_red')
        objects.append(player)
        while True:
            character.moveCursor()
            character.move()
            character.render()

            player.moveCursor()
            player.move()
            player.render()
            root.update()
