try:
    from Tkinter import *
except:
    from tkinter import *

import random
import time

root = Tk()
root.config(cursor = "none")

class Game:
    def __init__(self):
        self.objects = []
        self.startTime = time.time()
        self.time = self.startTime - time.time()
        self.colors = ['green','orange','black','purple','white']
        self.bgColor = self.colors[random.randint(0,len(self.colors)-1)]
        self.noWin = True
        self.startLoop = False
        self.lastUpdate = 0
        self.firstUpdate = True
    def startMenu(self):
        canvas.create_text(root.winfo_screenwidth()/2,root.winfo_screenheight()/2 - 300,text = '''Fighting Climbers''',fill = "gray",font = ("TkTextFont",175))
        canvas.create_text(root.winfo_screenwidth()/2,root.winfo_screenheight()/2,text = '''p1 uses wasd to move and space bar to fire''',fill = "gray",font = ("TkTextFont",25))
        canvas.create_text(root.winfo_screenwidth()/2, root.winfo_screenheight()/2 + 50,text = '''p2 uses arrow keys to move and mouse to fire''',fill = "gray",font = ("TkTextFont",25))
        canvas.create_text(root.winfo_screenwidth()/2,root.winfo_screenheight()/2 + 300,text = '''Press any key to continue''',fill = "gray",font = ("TkTextFont",75))
    def playScreen(self):
        canvas.delete(ALL)
        enviroment.setRow(10)
        enviroment.setBlock(1,10,0)
        enviroment.setBlock(10,10,0)
        enviroment.setBlock(2,8)
        enviroment.setBlock(9,8)
        enviroment.setBlock(4,6)
        enviroment.setBlock(7,6)
        enviroment.setBlock(6,4)
        enviroment.setBlock(5,4)
        enviroment.setBlock(8,2)
        enviroment.setBlock(3,2)
        enviroment.render()

        canvas.create_rectangle(enviroment.rectSizex*0,enviroment.rectSizey*1,enviroment.rectSizex*1,enviroment.rectSizey*2,fill = 'gold')
        canvas.create_rectangle(enviroment.rectSizex*10,enviroment.rectSizey*1,enviroment.rectSizex*9,enviroment.rectSizey*2,fill = 'gold')

    def update(self):
        self.time = time.time() - self.startTime
        i = 0
        while i < len(self.objects):
            self.objects[i].move()
            self.objects[i].render()
            i += 1
        root.update()
        self.lastUpdate = self.time
    def winUpdate(self):
        self.time = time.time() - self.startTime
        i = 0
        while i < len(self.objects):
            self.objects[i].render()
            i += 1
        root.update()
        self.lastUpdate = self.time

    def startUpdate(self):
        self.time = time.time() - self.startTime
    def start(self,event):
        self.startLoop = True

    def win(self,winner):
        self.noWin = False
        canvas.create_text(root.winfo_screenwidth()/2,root.winfo_screenheight()/2,text = winner, fill = "gray",font = ("TkTextFont",100))
        canvas.create_text(root.winfo_screenwidth()/2,root.winfo_screenheight()/2 + 100,text = 'wins',fill = "gray",font = ("TkTextFont",100))

    def restart(self,event):
        self.noWin = True
        canvas.delete(ALL)
        player.restart()
        character.restart()
        enviroment.render()

        canvas.create_rectangle(enviroment.rectSizex*0,enviroment.rectSizey*1,enviroment.rectSizex*1,enviroment.rectSizey*2,fill = 'gold')
        canvas.create_rectangle(enviroment.rectSizex*10,enviroment.rectSizey*1,enviroment.rectSizex*9,enviroment.rectSizey*2,fill = 'gold')

class Enviroment:
    def __init__(self,sizex,sizey):
        self.color = game.colors[random.randint(0,len(game.colors)-1)]
        while self.color == game.bgColor:
            self.color = game.colors[random.randint(0,len(game.colors)-1)]
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
        if game.startLoop:
            self.render()
    def setRow(self,x,on=1):
        i = 0
        while i < self.sizex:
            self.grid[x-1][i] = on
            i += 1
        if game.startLoop:
            self.render()
    def setColumn(self,y,on=1):
        i = 0
        while i < self.sizey:
            self.grid[i][y-1] = on
            i += 1
        if game.startLoop:
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
                    canvas.create_rectangle((z+1)*self.rectSizex,(i+1)*self.rectSizey,z*self.rectSizex,i*self.rectSizey,fill=self.color)
                z += 1
            i += 1
class Character:
    def __init__(self,name,left,right,jump,moveAim,gunInput,file):
        self.screenwidth = root.winfo_screenwidth()
        self.screenheight = root.winfo_screenheight()
        self.maxVelX = 1
        self.maxVelY = .5
        self.jumpAble = True
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
        self.speedx = self.screenwidth/2500
        self.originalspeedx = self.speedx
        self.speedy = root.winfo_screenheight()/100
        self.originalspeedy = self.speedy
        self.x = root.winfo_screenwidth()/2
        self.y = enviroment.rectSizey * 7
        self.originaly = self.y
        self.originalx = self.x
        self.cursorX = self.x
        self.cursorY = self.y
        if not 'none_' in file:
            self.file = file
            self.avatarBlue = PhotoImage(file = file)
            self.avatarBlueNewSizeX = round(self.size/self.avatarBlue.width())
            self.avatarBlueNewSizeY = round(self.size/self.avatarBlue.height())
            #self.avatarBlue = self.avatarBlue.subsample(int(1),int(self.avatarBlueNewSizeY)/2)
            self.avatarBlue = self.avatarBlue.zoom(int(self.avatarBlueNewSizeX),int(self.avatarBlueNewSizeY))
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
        self.originalJumpSpeed = self.jumpSpeed
        self.gravSpeed = root.winfo_screenheight()/1500
        self.originalGravSpeed = self.gravSpeed
        self.hit = 0
        self.stillHit = 0
        self.velocityX = 0
        self.velocityY = 0
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
            spoty = (self.y + self.size/2)/enviroment.rectSizey
            spot_x_leftside = (self.x - self.size/2)/enviroment.rectSizex
            spot_x_rightside = (self.x + self.size/2)/enviroment.rectSizex
            if enviroment.grid[int(spoty)][int(spot_x_leftside)] == 1 or enviroment.grid[int(spoty)][int(spot_x_rightside)] == 1:
                self.jump = True

    def stopMove(self,event):

        if event.keysym in self.leftInput:
            self.left = False
        if event.keysym in self.rightInput:
            self.right = False

    def move(self):
        self.speedx = self.originalspeedx * ((game.time - game.lastUpdate)/0.015)
        self.jumpSpeed = self.originalJumpSpeed * ((game.time - game.lastUpdate)/0.015)
        self.gravSpeed = self.originalGravSpeed * ((game.time - game.lastUpdate)/0.015)

        spoty = (self.y + self.size/2)/enviroment.rectSizey
        spot_y_middle = (self.y + self.size/3)/enviroment.rectSizey
        spot_y_top = (self.y - self.size/2)/enviroment.rectSizey
        spot_x_middle = (self.x)/enviroment.rectSizex
        spot_x_leftside = (self.x - self.size/2)/enviroment.rectSizex
        spot_x_rightside = (self.x + self.size/2)/enviroment.rectSizex

        if (int(spot_x_rightside) == 0 and int(spoty) == 9) or (int(spot_x_leftside) == 9 and int(spoty) == 9):
            self.x = self.originalx
            self.y = self.originaly
            self.hit = 0
        if int(spot_x_middle) == 0 and int(spot_y_top) == 1:
            if self.name == 0:
                game.win('blue')
            else:
                game.win('red')
        if int(spot_x_middle) == 9 and int(spot_y_top) == 1:
            if self.name == 0:
                game.win('blue')
            else:
                game.win('red')
        if self.hit == 0:
            if self.left:
                self.velocityX -= self.speedx

            if self.right:
                self.velocityX += self.speedx

            if not self.right and not self.left:
                self.velocityX = 0

        else:
            if self.stillHit <= 500:
                if self.x < root.winfo_screenwidth() - self.size and self.x > 0 + self.size:
                    self.velocityX += self.speedx * 2 * self.hit
                #else:
                    #self.stillHit = 0
                self.stillHit += 1
            else:
                self.hit = 0
        if self.jump:
            if self.jumped < enviroment.rectSizey*2.75 and self.y - self.size/2 > 0:
                self.velocityY -= self.jumpSpeed
                self.jumped += self.jumpSpeed
            else:
                self.velocityY = 0
                self.jump = False
                self.jumped = 0

        if (not enviroment.grid[int(spoty)][int(spot_x_leftside)] == 1 and not enviroment.grid[int(spoty)][int(spot_x_rightside)] == 1) and not self.jump:
            self.velocityY += self.gravSpeed
        else:
            if not self.jump:
                self.velocityY = 0

            self.jumpAble = True
        i = 0
        while i < len(game.objects)-1:
            if not i == self.name:
                other = game.objects[i]
                if self.x + self.size/2 > other.x - other.size/2 and (not self.x > other.x) and (self.y - self.size/2 < other.y + other.size/2 and self.y + self.size/2 > other.y - other.size/2):
                    self.stillHit = 0
                    self.hit = -.2
                    other.stillHit = 0
                    other.hit = .2

                if self.x - self.size/2 < other.x + other.size/2 and (not self.x < other.x) and (self.y - self.size/2 < other.y + other.size/2 and self.y + self.size/2 > other.y - other.size/2):
                    self.stillHit = 0
                    self.hit = .2
                    other.stillHit = 0
                    other.hit = -.2

            i += 1
        if self.velocityX > self.maxVelX:
            self.velocityX -= self.speedx
        if self.velocityX < -self.maxVelX:
            self.velocityX += self.speedx

        if self.velocityY > self.maxVelY:
            self.velocityY -= self.gravSpeed
        if self.velocityY < -self.maxVelY:
            self.velocityY += self.jumpSpeed

        if self.x > 0 + self.size/2 + 1 and not self.x > self.screenwidth - (self.size/2) - 1:
            self.x += self.velocityX
        else:
            self.velocityX = -self.velocityX
        if self.y > 0 + self.size/2 + 1 and not self.y > self.screenheight - (self.size) - 1:
            self.y += self.velocityY
        else:
            self.velocityY = -self.velocityY

        if enviroment.grid[int(spot_y_middle)][int(spot_x_leftside)] == 0:
            print('worling')
    def fire(self,event):
        if event.keysym in self.gunInput or self.gunInput == 'mouse_button':
            i = 0
            self.aimcolor = "black"
            self.aimcolorchange = time.time()
            while i < len(game.objects):
                if self.swordDirction == 1:
                    game.objects[i].isHit(range(int(self.x),int(self.x + self.swordLengthX*self.swordDirction)),self.y + self.size/2,self.y - self.size/2,self.swordDirction,self.name)
                else:
                    game.objects[i].isHit(range(int(self.x + self.swordLengthX*self.swordDirction),int(self.x)),self.y + self.size/2,self.y - self.size/2,self.swordDirction,self.name)
                i += 1
    def isHit(self,x,bottomY,topY,direction,name):
        if not self.name == name:
            for z in range(int(self.x - self.size/2),int(self.x + self.size/2)):
                if z in x:
                    if self.y <= bottomY and self.y >= topY:
                        if direction == -1:
                            self.stillHit = 0
                            self.hit = -1
                        else:
                            self.stillHit = 0
                            self.hit = 1

    def restart(self):
        self.x = self.originalx
        self.y = self.originaly

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

game = Game()

canvas = Canvas(root,width = root.winfo_screenwidth(),height = root.winfo_screenheight(),background = game.bgColor)
canvas.pack()

enviroment = Enviroment(10,10)

root.bind("<Key>",game.start)
root.update()

game.startMenu()

while game.startLoop == False:
    root.update()
    game.startUpdate()
    if game.startLoop == True:
        root.bind('<Return>',game.restart)

        game.playScreen()

        character = Character(0,['a'],['d'],['w','s'],['i','l','k','j'],['space'],'none_blue')
        game.objects.append(character)
        player = Character(1,['Left'],['Right'],['Up','Down'],'motion','mouse_button','none_red')
        game.objects.append(player)

        enviroment.createGrid()
        while True:
            while game.noWin:
                game.update()
            while not game.noWin:
                game.winUpdate()
