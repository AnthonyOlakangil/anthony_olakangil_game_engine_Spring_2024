# This file was created by: Anthony Olakangil

'''
Game design goals:
1. start screen/objective screen
2. weapon (done)
3. teleport (oone)
'''
# import necessary modules and libraries 
import pygame as pg 
import sys
from random import randint
from os import path
from settings import *
from sprites import *



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
        self.enemies = pg.sprite.Group()
        self.player = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.teleporters = pg.sprite.Group()
        self.boss = pg.sprite.Group()
        self.swords = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data): # function - creates tuples of 2 elements, tuple[0] being the index and tuple[1] being the actual element
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row) # create walls where there is a 1
                if tile == 'P':
                    self.player = Player(self, col, row) # initialize player wherever letter P is located on txt file
                if tile == 'E':
                    Enemy(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'Q':
                    Powerup(self, col, row)
                if tile == 'B':
                    Boss(self, col, row)
                if tile == 'S':
                    self.sword = Sword(self, col, row)
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
        self.teleporters.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE): 
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT)) # create vertical lines
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y)) # create horizontal lines


    def draw_text(self, text, font_name, size, color, x, y):
        font = pg.font.Font(pg.font.match_font(font_name), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y) # makes the topleft corner of the rectangle the (x,y) coords
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        if self.player.allowed:
            for row, tiles in enumerate(self.map_data): # function - creates tuples of 2 elements, tuple[0] being the index and tuple[1] being the actual element
                for col, tile in enumerate(tiles):
                    if tile == 'T':
                        Teleporter(self, col, row)
                        self.teleporters.draw(self.screen)
        self.draw_text(str(self.player.lives), "arial", 50, BLACK, 10, 10)
        self.draw_text(str(self.player.moneybag), "arial", 50, BLACK, 900, 10)
        pg.display.flip()

    # get user input
    def events(self):
        for event in pg.event.get(): # check for user input
            if event.type == pg.QUIT: # press the 'x' and exit application
                self.quit()
    
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
        

# instantiating the Game class
g = Game()
while True:
    g.new()
    g.run()
