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
class Character:
    def __init__(self,left,right,jump,file):
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

        root.bind("<Button-1>", self.fire)
        root.bind('<KeyPress>', self.changeMove)
        root.bind('<KeyRelease>', self.stopMove)

    def changeMove(self,event):
        print(self)
        if event.char in self.leftInput:
            self.left = True
        if event.char in self.rightInput:
            self.right = True
        if event.char in self.jumpInput:
            self.jump = True

    def stopMove(self,event):
        if event.char == "a":
            self.left = False
        if event.char == "d":
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
                    self.y -= 1
                    self.jumped += 1
                else:
                    self.jump = False
                    self.jumped = 0
        if not self.y == self.originaly and not self.jump:
            self.y += 1
        '''if self.down:
            if self.y < root.winfo_screenheight() - self.size/2:
                self.y += self.speedy
        if self.up:
            if self.y > 0 + self.size/2:
                self.y -= self.speedy'''
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
    '''    while i < len(enemys):
            enemy = enemys[i]
            if self.cursorX < enemy.x + enemy.size and self.cursorX > enemy.x - enemy.size and self.cursorY < enemy.y + enemy.size and self.cursorY > enemy.y - enemy.size:
                score.score += int(10/(time.time() - enemy.timeborn))
                enemy.hit()'''

            #i += 1
    def isHit(self):
        r = 0
        while r < len(enemys):
            enemy = enemys[r]
            if enemy.y + enemy.size >= self.y - self.size or (enemy.x + enemy.size >= self.x - self.size and enemy.x + enemy.size >= self.x - self.size) or enemy.x - enemy.size <= self.x + self.size:
                self.dead = True
            r += 1
    def render(self):
        canvas.delete(self.graphics)
        canvas.delete(self.aim)
        if time.time() - self.aimcolorchange > .1:
            self.aimcolor = "gray"
            self.aimcolorchange = 0
        if not self.dead:
            self.aim = canvas.create_line(self.x,self.y,self.cursorX,self.cursorY,fill = self.aimcolor,width = 10)
            #self.graphics = canvas.create_rectangle(self.x - self.size/2,self.y - self.size/2,self.x + self.size/2,self.y + self.size/2,fill = "green")
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
        character = Character(['a'],['d'],['w','s'])
        player = Character(['<left>'],['<right>'],['<up>','<down>'])

        while True:
            character.moveCursor()
            character.move()
            character.render()

            player.moveCursor()
            player.move()
            player.render()
            root.update()
