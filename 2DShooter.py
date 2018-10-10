from tkinter import *
import random
import time

root = Tk()
root.config(cursor = "none")

canvas = Canvas(root,width = root.winfo_screenwidth(),height = root.winfo_screenheight(),background = "black")
canvas.pack()

canvas.create_text(root.winfo_screenwidth()/2,root.winfo_screenheight()/2 - 300,text = '''2DShooter.py''',fill = "white",font = ("TkTextFont",175))
canvas.create_text(root.winfo_screenwidth()/2,root.winfo_screenheight()/2,text = '''press left mouse to fire''',fill = "gray7",font = ("TkTextFont",25))
canvas.create_text(root.winfo_screenwidth()/2, root.winfo_screenheight()/2 + 50,text = '''move mouse to aim''',fill = "gray7",font = ("TkTextFont",25))
canvas.create_text(root.winfo_screenwidth()/2,root.winfo_screenheight()/2 + 300,text = '''Press any key to continue''',fill = "gray7",font = ("TkTextFont",75))

startTime = time.time()
startLoop = False
class Score:
    def __init__(self):
        self.score = 0
        self.scoreText = canvas.create_text(root.winfo_screenwidth()/2,100,text = self.score,font = 100)
        canvas.create_text(root.winfo_screenwidth()/3,100,text = "Score: ",font = ('TkTextFont',100),fill = "white")
class Character:
    def __init__(self):
        self.size = root.winfo_screenwidth()/25
        self.dead = False
        self.left = False
        self.right = False
        self.down = False
        self.up = False
        self.aimcolor = "blue"
        self.aimcolorchange = 0
        self.speedx = root.winfo_screenwidth()/250
        self.speedy = root.winfo_screenheight()/250
        self.x = root.winfo_screenwidth()/2
        self.y = (root.winfo_screenheight()/100)*92 - self.size/2
        self.cursorX = self.x
        self.cursorY = self.y
        self.avatarBlue = PhotoImage(file = "avatarBlue.gif")
        self.avatarBlueNewSize = int(self.avatarBlue.width()/self.size)
        self.avatarBlue = self.avatarBlue.subsample(self.avatarBlueNewSize)
        self.gunStrength = root.winfo_screenwidth()/5
        self.graphics = canvas.create_rectangle(self.x - self.size/2,self.y - self.size/2,self.x + self.size/2,self.y - self.size/2)
        self.aim = canvas.create_line(self.x,self.y,self.x,self.y)
    def changeMove(self,event):
        if event.char == "a":
            self.left = True
        if event.char == "d":
            self.right = True
        if event.char == "s":
            self.down = True
        if event.char == "w":
            self.up = True
    def stopMove(self,event):
        if event.char == "a":
            self.left = False
        if event.char == "d":
            self.right = False
        if event.char == "s":
            self.down = False
        if event.char == "w":
            self.up = False
    def move(self):
        if self.left:
            if self.x > 0 + self.size/2:
                self.x -= self.speedx
        if self.right:
            if self.x < root.winfo_screenwidth() - self.size/2:
                self.x += self.speedx
        if self.down:
            if self.y < root.winfo_screenheight() - self.size/2:
                self.y += self.speedy
        if self.up:
            if self.y > 0 + self.size/2:
                self.y -= self.speedy
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
        self.aimcolor = "green"
        self.aimcolorchange = time.time()
        while i < len(enemys):
            enemy = enemys[i]
            if self.cursorX < enemy.x + enemy.size and self.cursorX > enemy.x - enemy.size and self.cursorY < enemy.y + enemy.size and self.cursorY > enemy.y - enemy.size:
                score.score += int(10/(time.time() - enemy.timeborn))
                enemy.hit()

            i += 1
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
            self.aimcolor = "blue"
            self.aimcolorchange = 0
        if not self.dead:
            self.aim = canvas.create_line(self.x,self.y,self.cursorX,self.cursorY,fill = self.aimcolor,width = 10)
            #self.graphics = canvas.create_rectangle(self.x - self.size/2,self.y - self.size/2,self.x + self.size/2,self.y + self.size/2,fill = "green")
            self.graphics = canvas.create_image(self.x,self.y,image = self.avatarBlue)

class Enemy:
    def __init__(self):
        self.timeborn = time.time()
        self.size = root.winfo_screenwidth()/25
        self.dead = False
        self.avatarRed = PhotoImage(file = "avatarRed.gif")
        self.avatarRedNewSize = int(self.avatarRed.width()/self.size)
        self.avatarRed = self.avatarRed.subsample(self.avatarRedNewSize)
        self.x = random.randint(0,root.winfo_screenwidth())
        self.y = random.randint(0,root.winfo_screenheight())
        self.originalx = self.x
        self.originaly = self.y
        self.jumpheight = self.size * 3
        self.graphics = canvas.create_rectangle(self.x - self.size/2,self.y - self.size/2,self.x + self.size/2,self.y - self.size/2)
    def jump(self):
        if self.y == self.originaly and self.x == self.originalx:
            self.modifier = random.randint(-1,1)
            self.direction = random.randint(1,2)
            while self.modifier == 0:
                self.modifier = random.randint(-1,1)

            if self.direction == 2:
                self.y += self.jumpheight*self.modifier
            else:
                self.x += self.jumpheight*self.modifier

    def gravity(self):
        if self.y < (root.winfo_screenheight()/100)*92:
            self.y += 3
    def render(self):
        canvas.delete(self.graphics)
        if not self.dead:
            self.graphics = canvas.create_image(self.x,self.y,image = self.avatarRed)
    def hit(self):
        self.dead = True
        self.y = 1000000
def start(event):
    global startLoop
    startLoop = True
root.bind("<Key>",start)
root.update()
while startLoop == False:
    root.update()
    if startLoop == True:
        canvas.delete(ALL)
        character = Character()
        enemys = [Enemy()]
        score = Score()

        root.bind("<Button-1>",character.fire)
        root.bind('<KeyPress>',character.changeMove)
        root.bind('<KeyRelease>', character.stopMove)
        #root.bind("<Motion>",caracter.moveCursor)
        while True:
            if time.time() > startTime + len(enemys)*1:
                enemys.append(Enemy())
                timeEnemyAdded = time.time()
            r = 0
            while r < len(enemys):
                enemys[r].jump()
                enemys[r].gravity()
                enemys[r].render()
                r += 1

            canvas.delete(score.scoreText)
            score.scoreText = canvas.create_text(root.winfo_screenwidth()/2,100,text = score.score,fill = "white",font = ('TkTextFont',100))
            character.moveCursor()
            character.move()
            #character.isHit()
            character.render()
            root.update()
