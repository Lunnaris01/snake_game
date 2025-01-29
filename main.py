from graphics import Window, Map, Snake
from tkinter import Event
def main():
    cellsize = 16
    gameheight = 40
    gamewidth = 40
    win = Window(cellsize*gameheight,cellsize*gamewidth)
    snake = Snake(gameheight//2,gamewidth//2,win)
    game_map = Map(win,snake,cellsize)
    game_map.draw(win.canvas)
    game_map.draw_snake()
    snake.set_map(game_map)
    win.set_map(game_map)
    game_map.game_start()


    win.wait_for_close()






if __name__  == '__main__':
    main()