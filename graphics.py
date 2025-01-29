from tkinter import Tk, BOTH, Canvas,Event
import time
import random
from enum import Enum

class FieldType(Enum):
    EMPTY = 0
    WALL = 1
    FOOD = 2
    SNAKE = 3

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
        self.root.bind('<Left>',self.leftKey)
        self.root.bind('d', self.rightkey)
        self.root.bind('<Right>',self.rightkey)
        self.paused = False

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
        
    def close(self):
        self.running = False

class Map():
    def __init__(self,win:Window, snake, cellsize = 16):
        self.cellsize = cellsize
        self.snake = snake
        self.width = win.width//self.cellsize
        self.height = win.height//self.cellsize
        self.fields = [[FieldType.EMPTY for _ in range(self.width)] for _ in range(self.height)]
        self.init_field()
        self.win = win
        self.set_next_food()
        self.draw(win.canvas)

    def init_field(self):
        self.fields[0] = [FieldType.WALL for _ in range(self.width)]
        self.fields[-1] = [FieldType.WALL for _ in range(self.width)]
        for j in range(self.height):
            self.fields[j][0] = FieldType.WALL
            self.fields[j][-1] = FieldType.WALL

    def set_next_food(self):
        x,y = (random.randint(1,self.width-1),random.randint(1,self.height-1))
        while (self.fields[x][y] != FieldType.EMPTY):
            x,y = random.randint(1,self.width-1),random.randint(1,self.height-1)
        self.fields[x][y] = FieldType.FOOD
        print(x,y)

    def draw(self,canvas:Canvas,color="black"):
        for i in range(self.width):
            for j in range(self.height):
                if self.fields[j][i] == FieldType.WALL:
                    canvas.create_rectangle(i*self.cellsize,j*self.cellsize,(i+1)*self.cellsize,(j+1)*self.cellsize,fill="black")
                elif self.fields[j][i] == FieldType.FOOD:
                    canvas.create_rectangle(i*self.cellsize,j*self.cellsize,(i+1)*self.cellsize,(j+1)*self.cellsize,fill="red",stipple="gray25")
                elif self.fields[j][i] == FieldType.SNAKE:
                    canvas.create_rectangle(i*self.cellsize,j*self.cellsize,(i+1)*self.cellsize,(j+1)*self.cellsize,outline= "green",fill="green")
                elif self.fields[j][i] == FieldType.EMPTY:
                    canvas.create_rectangle(i*self.cellsize,j*self.cellsize,(i+1)*self.cellsize,(j+1)*self.cellsize,outline="white",fill="white")

    def animate(self):
        self.win.redraw()
        time.sleep(0.1)

    def game_start(self):
        while(not self.snake.crashed):
            if not self.win.paused:
                self.animate()
                self.snake.move()
            self.draw(self.win.canvas)

        self.win.running = False


class Snake():
    def __init__(self,startx,starty,win):
        self.snake_draw = [(startx,starty)]
        self.crashed = False
        self.win = win
        self.map = None
        self.directiontupel = (0,1)
    
    def set_map(self,map):
        self.map = map

    def move(self):
        nextpos = add_tupel(self.snake_draw[-1],self.directiontupel)
        if self.map.fields[nextpos[0]][nextpos[1]] == FieldType.WALL or self.map.fields[nextpos[0]][nextpos[1]] == FieldType.SNAKE:
            self.crashed = True
            print(f"Crashed at {nextpos}")
        
        if self.map.fields[nextpos[0]][nextpos[1]] == FieldType.FOOD:
            self.map.nextfood = self.map.set_next_food()
        else:
            x,y = self.snake_draw.pop(0)
            self.map.fields[x][y] = FieldType.EMPTY

        self.snake_draw.append(nextpos)
        self.map.fields[nextpos[0]][nextpos[1]] = FieldType.SNAKE

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