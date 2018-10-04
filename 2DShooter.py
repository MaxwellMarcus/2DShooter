from tkinter import *
import random
import time

root = Tk()

canvas = Canvas(root,width = root.winfo_screenwidth(),height = root.winfo_screenheight(),background = "black")
canvas.pack()

startTime = time.time()
class Character:
    def __init__(self):
        self.size = 50
        self.x = root.winfo_screenwidth()/2
        self.y = (root.winfo_screenheight()/100)*92 - self.size/2
        self.cursorX = self.x
        self.cursorY = self.y
        self.gunStength = 400
        self.graphics = self.graphics = canvas.create_rectangle(self.x - self.size/2,self.y - self.size/2,self.x + self.size/2,self.y + self.size/2,fill = "red")
        self.aim = canvas.create_line(self.x,self.y,self.x,self.y)
    def moveLeft(self,event):
        self.x -= 10

    def moveRight(self,event):
        self.x += 10

    def moveCursor(self,event):
        if not event.x > self.x + self.gunStength or not event.x < self.x - self.gunStength or not event.y > self.y + self.gunStength or not event.y < self.y - self.gunStength:
            self.cursorX = event.x
            self.cursorY = event.y
    def fire(self,event):
        i = 0
        while i < len(enemys):
            enemy = enemys[i]
            if self.cursorX < enemy.x + enemy.size and self.cursorX > enemy.x - enemy.size and self.cursorY < enemy.y + enemy.size and self.cursorY > enemy.y - enemy.size:
                enemy.hit()
            i += 1
    def render(self):
        canvas.delete(self.graphics)
        canvas.delete(self.aim)
        self.aim = canvas.create_line(self.x,self.y,self.cursorX,self.cursorY,fill = "blue")
        self.graphics = canvas.create_rectangle(self.x - self.size/2,self.y - self.size/2,self.x + self.size/2,self.y + self.size/2,fill = "red")

class Enemy():
    def __init__(self):
        self.size = 50
        self.dead = False
        self.x = random.randint(0,root.winfo_screenwidth())
        self.y = (root.winfo_screenheight()/100)*92 - self.size/2
        self.graphics = self.graphics = canvas.create_rectangle(self.x - self.size/2,self.y - self.size/2,self.x + self.size/2,self.y + self.size/2,fill = "green")
    def jump(self):
        if self.y == (root.winfo_screenheight()/100)*92 - self.size/2:
            self.y -= 200
    def gravity(self):
        if self.y > (root.winfo_screenheight()/100)*92:
            self.y += 1
    def render(self):
        canvas.delete(self.graphics)
        if not self.dead:
            self.graphics = canvas.create_rectangle(self.x - self.size/2,self.y - self.size/2,self.x + self.size/2,self.y + self.size/2,fill = "green")
    def hit(self):
        self.dead = True
character = Character()
enemys = [Enemy()]

root.bind("a",character.moveLeft)
root.bind("d",character.moveRight)
root.bind("<Motion>",character.moveCursor)
root.bind("<Button-1>",character.fire)

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
    character.render()
    root.update()
