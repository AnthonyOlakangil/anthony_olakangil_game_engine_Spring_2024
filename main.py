# This file was created by: Anthony Olakangil

'''
Game design goals:
1. start screen/objective screen (done)
2. weapon (done)
3. teleport (done)
4. die screen/game over (done)
5. respawn option if gameover (done)
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
        self.enemy_count = 0
        self.waiting = None
 
 
     # load save game data etc
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f: # reading map.txt
            for line in f:
                self.map_data.append(line) # loading all contents from txt file into array to be used in 'new' method
        
    def show_start_screen(self):
        self.screen.fill(SILVER)
        self.draw_text("Your Objectives:", "impact", 30, BLACK, WIDTH/2, (HEIGHT/2)-110)
        self.draw_text("-Kill all static guards", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)-50)
        self.draw_text("-Unlock the teleporter", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)-20)
        self.draw_text("-Evade or fight the mob boss", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)+10)
        self.draw_text("    -Don't get too close!", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)+40)
        self.draw_text("-Use powerups to speed away", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)+70)
        self.draw_text("Don't die!", "impact", 30, BLACK, WIDTH/2, (HEIGHT/2)+110)
        self.draw_text("Press any key to start", "couriernew", 30, BLACK, WIDTH/2, (HEIGHT/2)+210)
        pg.display.flip()
        self.wait_for_key()
    
    def show_end_screen(self):
        self.screen.fill(RED)
        self.draw_text("YOU DIED!", "impact", 30, BLACK, WIDTH/2, HEIGHT/2)
        self.draw_text("press any key to restart", "couriernew", 30, BLACK, WIDTH/2, (HEIGHT/2)+50)
        pg.display.flip()
        self.wait_for_key()


    def wait_for_key(self):
        self.waiting = True
        while self.waiting:
            # wait 1/30th second to maintain consistent FPS
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYUP: # 'click to start' functionality
                    self.waiting = False
    
    def new(self):
        # init all variables, set up groups, instantiate classes etc
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
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
                    self.enemy_count += 1
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'Q':
                    Powerup(self, col, row)
                if tile == 'B':
                    Boss(self, col, row)
                if tile == 'S':
                    self.sword = Sword(self, col, row)
    def run(self):
        self.show_start_screen()
        self.playing = True
        # if they have clicked to start/restart
        if not self.waiting:
            while self.playing:
                self.dt = self.clock.tick(FPS) / 1000 # convert to seconds
                self.events()
                self.update()
                self.draw()
                if self.player.dead:
                    self.show_end_screen()
                    # reinstantiate player
                    self.new()
                    # redisplay start screen/restart game
                    # recursion
                    self.run()


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
        text_rect.center = (x, y) # makes the topleft corner of the rectangle the (x,y) coords
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        if self.enemy_count == 0:
            for row, tiles in enumerate(self.map_data): # function - creates tuples of 2 elements, tuple[0] being the index and tuple[1] being the actual element
                for col, tile in enumerate(tiles):
                    if tile == 'T':
                        self.teleporter = Teleporter(self, col, row)
                        self.teleporters.draw(self.screen)

        self.draw_text(str(self.player.lives), "arial", 50, BLACK, 50, 25)
        self.draw_text(str(self.player.moneybag), "arial", 50, BLACK, 975, 30)
        pg.display.flip()

    # get user input
    def events(self):
        for event in pg.event.get(): # check for user input
            if event.type == pg.QUIT: # press the 'x' and exit application
                self.quit()
    

# instantiating the Game class
g = Game()
while True:
    g.new()
    g.run()
