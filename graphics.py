from tkinter import Tk, BOTH, Canvas,Event
import time
import random
from enum import Enum

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class Window():
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title = "Mazesolver"
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.root,bg = 'white',height=self.height,width=self.width)
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False
        self.root.bind('a', self.leftKey)
        self.root.bind('d', self.rightkey)
        self.map = None

    def set_map(self,map):
        self.map = map

    def leftKey(self,event):
        self.map.snake.changedir(Direction.LEFT)

    def rightkey(self,event):
        self.map.snake.changedir(Direction.RIGHT)


    def redraw(self):
        self.root.update_idletasks()
        self.root.update()
        
    def wait_for_close(self):
        self.running = True
        while(self.running):
            self.redraw()

    def close(self):
        self.running = False

class Map():
    def __init__(self,win:Window, snake, cellsize = 16):
        self.cellsize = cellsize
        self.snake = snake
        self.width = win.width//self.cellsize
        self.height = win.height//self.cellsize
        self.fields = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.init_field()
        self.win = win
        self.draw_snake()
        self.nextfood = self.set_next_food()
        self.draw_food()

    def draw_snake(self):
        for x,y in self.snake.snake_draw:
            self.fields[x][y] = 1
            self.win.canvas.create_rectangle(x*self.cellsize,y*self.cellsize,(x+1)*self.cellsize,(y+1)*self.cellsize,outline= "green",fill="green")
        for x,y in self.snake.snake_undraw:
            self.fields[x][y] = 0
            self.win.canvas.create_rectangle(x*self.cellsize,y*self.cellsize,(x+1)*self.cellsize,(y+1)*self.cellsize,outline="white",fill="white")
            self.snake.snake_undraw = []

    def draw_food(self):
        self.win.canvas.create_rectangle(self.nextfood[0]*self.cellsize,self.nextfood[1]*self.cellsize,(self.nextfood[0]+1)*self.cellsize,(self.nextfood[1]+1)*self.cellsize,fill="red",stipple="gray25")

    def init_field(self):
        self.fields[0] = [1 for _ in range(self.width)]
        self.fields[-1] = [1 for _ in range(self.width)]
        for j in range(self.height):
            self.fields[j][0] = 1
            self.fields[j][-1] = 1

    def set_next_food(self):
        x,y = (random.randint(1,self.width-1),random.randint(1,self.height-1))
        while (self.fields[x][y]):
            x,y = (random.randint(1,self.width-1),random.randint(1,self.height-1))
        self.fields[x][y] = 2
        return (x,y)


    def draw(self,canvas:Canvas,color="black"):
        for i in range(self.width):
            for j in range(self.height):
                if self.fields[j][i] == 1:
                    canvas.create_rectangle(i*self.cellsize,j*self.cellsize,(i+1)*self.cellsize,(j+1)*self.cellsize,fill=color)
                elif self.fields[j][i] == 2:
                    canvas.create_rectangle(self.nextfood[0]*self.cellsize,self.nextfood[1]*self.cellsize,(self.nextfood[0]+1)*self.cellsize,(self.nextfood[1]+1)*self.cellsize,fill="red",stipple="gray25")


    def animate(self):
        self.win.redraw()
        time.sleep(0.1)

    def game_start(self):
        while(not self.snake.crashed):
            self.animate()
            self.snake.move()
            self.draw_snake()
        self.win.running = False


class Snake():
    def __init__(self,startx,starty,win):
        self.snake_draw = [(startx,starty)]
        self.snake_undraw = []
        self.has_eaten = False
        self.crashed = False
        self.win = win
        self.map = None
        self.directiontupel = (0,1)

    def animate(self):
        self.win.redraw()
        time.sleep(0.1)
    
    def set_map(self,map):
        self.map = map

    def move(self):
        nextpos = add_tupel(self.snake_draw[-1],self.directiontupel)
        if self.map.fields[nextpos[0]][nextpos[1]] == 1:
            self.crashed = True
            print(f"Crashed at {nextpos}")
        
            self.has_eaten = True
        self.snake_draw.append(nextpos)
        if self.map.fields[nextpos[0]][nextpos[1]] != 2:
            self.snake_undraw.append(self.snake_draw.pop(0))
        self.has_eaten = False
        self.map.set_next_food()

    def changedir(self,direction):
        if direction == Direction.LEFT:
            print(self.directiontupel)
            if self.directiontupel == (0,1):
                self.directiontupel = (1,0)
            elif self.directiontupel == (0,-1):
                self.directiontupel = (-1,0)
            elif self.directiontupel == (1,0):
                self.directiontupel = (0,-1)
            elif self.directiontupel == (-1,0):
                self.directiontupel = (0,1)
        elif direction == Direction.RIGHT:
            if self.directiontupel == (0,1):
                self.directiontupel = (-1,0)
            elif self.directiontupel == (0,-1):
                self.directiontupel = (1,0)
            elif self.directiontupel == (1,0):
                self.directiontupel = (0,1)
            elif self.directiontupel == (-1,0):
                self.directiontupel = (0,-1)

def add_tupel(x,y):
    return (x[0]+y[0],x[1]+y[1])