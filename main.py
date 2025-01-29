from graphics import Window, Map, Snake
from tkinter import Event
def main():
    cellsize = 16
    gameheight = 40
    gamewidth = 40
    win = Window(cellsize*gameheight,cellsize*gamewidth)
    snake = Snake(gameheight//2,gamewidth//2,win)
    game_map = Map(win,snake,cellsize)
    snake.set_map(game_map)
    win.set_map(game_map)
    game_map.game_start()







if __name__  == '__main__':
    main()