# This file was created by: Anthony Olakangil

# import necessary modules and libraries 
import pygame as pg 
import sys
from random import randint
from os import path
from time import sleep
from settings import *
from sprites import *

def draw_text():
    pass

# Create the Game class
class Game:
    # initialize the window settings
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.running = True
 
 
     # load save game data etc
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f: # reading map.txt
            for line in f:
                self.map_data.append(line) # loading all contents from txt file into array to be used in 'new' method

        
    
    def new(self):
        # init all variables, set up groups, instantiate classes etc
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.enemy = pg.sprite.Group()
        # create player object - top left corner will be (10,10)
        # self.player = Player(self, 10, 10)
        # create 10 unit rectangle
        # for x in range(10, 20):
            # Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data): # function - creates tuples of 2 elements, tuple[0] being the index and tuple[1] being the actual element
            print(tiles)
            for col, tile in enumerate(tiles):
                print(tile)
                if tile == '1':
                    Wall(self, col, row) # create walls where there is a 1
                if tile == 'P':
                    self.player = Player(self, col, row) # initialize player wherever letter P is located on txt file
                if tile == 'E':
                    Enemy(self, col, row)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 # convert to seconds
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit() # close pygame
        sys.exit() # kill python program
        
    def update(self):
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE): 
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT)) # create vertical lines
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y)) # create horizontal lines

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    # get user input
    def events(self):
        for event in pg.event.get(): # check for user input
            if event.type == pg.QUIT: # press the 'x' and exit application
                self.quit()
    #         if event.type == pg.KEYDOWN: # using keyboard/mouse
    #             # checking for keyboard events
    #             # keysym of Left arrow key
    #             if event.key == pg.K_LEFT:
    #                 self.player.move(dx=-1)
    #             # keysym of Right arrow key
    #             if event.key == pg.K_RIGHT:
    #                 self.player.move(dx=1)
    #             # moving up
    #             if event.key == pg.K_UP:
    #                 self.player.move(dy=-1)
    #             # moving down
    #             if event.key == pg.K_DOWN:
    #                 self.player.move(dy=+1)
    
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
        

# instantiating the Game class
g = Game()
# g.show_start_screen
while True:
    g.new()
    g.run()
    # g.show_go_screen()

# calling the run method
