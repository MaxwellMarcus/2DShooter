from tkinter import *
import random
import time

root = Tk()

canvas = Canvas(root,width = root.winfo_screenwidth(),height = root.winfo_screenheight(),background = "black")
canvas.pack()

avatarBlue = PhotoImage("avatarBlue.gif")
avatarRed = PhotoImage("avatarRed.gif")
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
        canvas.create_text(root.winfo_screenwidth()/3,100,text = "Scrore: ",font = ('TkTextFont',100),fill = "white")
class Character:
    def __init__(self):
        self.size = 50
        self.dead = False
        self.x = root.winfo_screenwidth()/2
        self.y = (root.winfo_screenheight()/100)*92 - self.size/2
        self.cursorX = self.x
        self.cursorY = self.y
        self.gunStength = 400
        self.graphics = canvas.create_image(self.x,self.y,image = avatarBlue)
        self.aim = canvas.create_line(self.x,self.y,self.x,self.y)
    def moveLeft(self,event):
        self.x -= 10
    def moveRight(self,event):
        self.x += 10

    def moveCursor(self,event):
        if event.x < self.x + self.gunStength and event.x > self.x - self.gunStength:
            self.cursorX = event.x
        if event.y < self.y + self.gunStength and event.y > self.y - self.gunStength:
            self.cursorY = event.y
    def fire(self,event):
        i = 0
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
        if not self.dead:
            self.aim = canvas.create_line(self.x,self.y,self.cursorX,self.cursorY,fill = "blue",width = 10)
            self.graphics = canvas.create_image(self.x,self.y)

class Enemy:
    def __init__(self):
        self.timeborn = time.time()
        self.size = 50
        self.dead = False
        self.x = random.randint(0,root.winfo_screenwidth())
        self.y = (root.winfo_screenheight()/100)*92 - self.size/2
        self.graphics = self.graphics = canvas.create_rectangle(self.x - self.size/2,self.y - self.size/2,self.x + self.size/2,self.y + self.size/2,fill = "green")
    def jump(self):
        if self.y >= (root.winfo_screenheight()/100)*92 - self.size/2:
            '''self.now = time.time()
            while time.time < self.now + 1:
                pass'''
            self.y -= 100
    def gravity(self):
        if self.y < (root.winfo_screenheight()/100)*92:
            self.y += 3
    def render(self):
        canvas.delete(self.graphics)
        if not self.dead:
            self.graphics = canvas.create_rectangle(self.x - self.size/2,self.y - self.size/2,self.x + self.size/2,self.y + self.size/2,fill = "green")
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

        root.bind("a",character.moveLeft)
        root.bind("d",character.moveRight)
        root.bind("<Button-1>",character.fire)
        root.bind("<Motion>",character.moveCursor)
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
        #    character.moveCursor()
            #character.isHit()
            character.render()
            root.update()
