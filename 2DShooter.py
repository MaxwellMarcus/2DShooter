from tkinter import *

root = Tk()

canvas = Canvas(root,width = root.winfo_screenwidth(),height = root.winfo_screenheight(),background = "black")
canvas.pack()

class Character:
    def setup(self):
        self.size = 50
        self.x = root.winfo_screenwidth()/2
        self.y = (root.winfo_screenheight()/100)*98 - self.size/2
        self.graphics = self.graphics = canvas.create_rectangle(self.x - self.size/2,self.y - self.size/2,self.x + self.size/2,self.y + self.size/2,fill = "red")
    def render(self):
        canvas.delete(self.graphics)
        self.graphics = canvas.create_rectangle(self.x - self.size/2,self.y - self.size/2,self.x + self.size/2,self.y + self.size/2,fill = "red")

character = Character()
character.setup()

while True:
    character.render()
    root.update()
