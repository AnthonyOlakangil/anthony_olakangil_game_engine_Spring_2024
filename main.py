# This file was created by: Anthony Olakangil with music debug from Aayush Sharma

'''
Game design goals:
1. start screen/objective screen (done)
2. weapon (done)
3. enemies (done)
4. boss (done)
5. coins (done)
6. speed powerup (done)
7. teleport (done)
8. die screen/game over (done)
9. respawn option if gameover (done)
10. sound (done)
11. spawn in buffed enemies in unbeatable stage (done)

BETA GOAL:
    (done)
    improve movement                    
    panning
    camera moving with character
    not seeing entire map at once
'''

# import necessary modules and libraries 
import pygame as pg 
import sys
from random import randint
from os import path
from pygame.sprite import Group
from settings import *
from sprites import *
from camera import *

# Create the Game class

class Game:
    # initialize the window settings
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        # access dir with ./
        self.load_data('./maps/map3.txt')
        self.running = True
        # initialize counters
        self.enemy_count = 0
        self.buffed_enemy_count = 0
        self.store = 0
        self.waiting = None
        # load some music
        self.sound = pg.mixer.Sound('./static/themesong.wav') 
 
     # load map file
    def load_data(self, file_name):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, file_name), 'rt') as f: # reading map.txt
            for line in f:
                self.map_data.append(line) # loading all contents from txt file into array to be used in 'new' method

  
        
    def show_start_screen(self):
        self.screen.fill(SILVER)
        # WIDTH/2 and HEIGHT/2 sets to middle of screen
        # arithmetic at the end is for paragraph formatting
        self.draw_text("Your Objectives:", "impact", 30, BLACK, WIDTH/2, (HEIGHT/2)-110)
        self.draw_text("-Kill all static guards", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)-50)
        self.draw_text("-Unlock the teleporter", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)-20)
        self.draw_text("-Evade or fight the mob boss", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)+10)
        self.draw_text("    -Don't get too close!", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)+40)
        self.draw_text("-Use powerups to speed away", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)+70)
        self.draw_text("Don't die!", "impact", 30, BLACK, WIDTH/2, (HEIGHT/2)+110)
        self.draw_text("Press any key to start", "couriernew", 30, BLACK, WIDTH/2, (HEIGHT/2)+210)
        self.draw_text("Press R to restart", "couriernew", 30, BLACK, WIDTH/2, (HEIGHT/2)+240)
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
                # 'click to start' functionality
                if event.type == pg.KEYUP: 
                    self.waiting = False
    
    def new(self):
        # init all variables, set up groups, instantiate classes etc
        self.sound.play(INDEFINITELY) # indefinite loop
        # initialize groups
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.teleporters = pg.sprite.Group()
        self.boss_group = pg.sprite.Group()
        self.swords = pg.sprite.Group()
        self.buffed_enemies = pg.sprite.Group()
        self.cameras = pg.sprite.Group
        self.magnets = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data): # enumerate - creates tuples of 2 elements, tuple[0] being the index and tuple[1] being the actual element
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row) # create walls where there is a 1
                if tile == 'P':
                    self.player = Player(self, col, row) # initialize player wherever letter P is located on txt file
                    self.camera = CameraGroup(self)
                if tile == 'E':
                    Enemy(self, col, row)
                    self.enemy_count += 1 # track how many enemies the game starts with
                if tile == 'C':
                    self.coin = Coin(self, col, row)
                    # print(len(coins_list))
                if tile == 'Q':
                    Powerup(self, col, row)
                if tile == 'B':
                    self.boss = Boss(self, col, row)
                if tile == 'S':
                    self.basic_sword = Basic_sword(self, col, row)
                if tile == 'R':
                    self.big_sword = Excalibur(self, col, row)
                if tile == 'G':
                    BuffedEnemy(self, col, row)
                    self.buffed_enemy_count += 1 # count how many buffed enemies the game starts with
                if tile == 'M':
                    self.magnet = Magnet(self, col, row)

    def stage_2(self):
        # load new level map
        self.load_data('./maps/map2.txt')
        self.new()  

    def show_new_screen(self):
        self.screen.fill(SILVER)
        self.draw_text("Level: INSANE", "impact", 30, BLACK, WIDTH/2, (HEIGHT/2)-140)
        self.draw_text("-all static guards have increased health and damage", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)-110)
        self.draw_text("    -Unlock the teleporter by killing them!", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)-80)
        self.draw_text("-There are multiple mob bosses.", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)-50)
        self.draw_text("    -There is no weapon upgrade. Collect all coins to complete level", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)-20)
        self.draw_text("    -Don't get too close!", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)+10)
        self.draw_text("-Use powerups to speed away", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)+40)
        self.draw_text("Don't die!", "impact", 30, BLACK, WIDTH/2, (HEIGHT/2)+100)
        self.draw_text("Press any key to start", "couriernew", 30, BLACK, WIDTH/2, (HEIGHT/2)+150)
        self.draw_text("Press R to restart", "couriernew", 30, BLACK, WIDTH/2, (HEIGHT/2)+180)
        pg.display.flip()
        self.wait_for_key()

    def show_finish_screen(self):
        self.screen.fill(SKYBLUE)
        self.draw_text("Level Complete!", "impact", 30, BLACK, WIDTH/2, (HEIGHT/2))
        self.draw_text("Press any key to play again", "couriernew", 30, BLACK, WIDTH/2, (HEIGHT/2)+150)
        pg.display.flip()
        self.wait_for_key()

                    
    def run(self):
        self.show_start_screen()
        self.playing = True
        # if they have clicked to start/restart
        if not self.waiting:
            # if the game isn't over
            if not self.boss.dead:
                # if window isn't closed
                while self.playing:
                    self.dt = self.clock.tick(FPS) / 1000 # convert to seconds
                    self.events()
                    self.update()
                    self.draw()
                    if self.player.dead:
                        self.show_end_screen()
                        # make sure that it recounts them from 0
                        self.enemy_count = 0
                        # re-draw map and all sprites
                        self.new()
                        # redisplay start screen/restart game
                        self.run()
                    # unequip everything for new level
                    if self.boss.dead:
                        self.player.weapon_basic = False
                        self.player.weapon_big = False
                        # store coins earned from level 1 before resetting it
                        self.store += self.player.moneybag
                        self.stage_2()
                        self.run_new_stage()
                        
    def run_new_stage(self):
        self.show_new_screen()
        self.playing = True
        if not self.waiting:
            # player retains all coins earned from previous level
            self.player.moneybag += self.store
            while self.playing:
                self.dt = self.clock.tick(FPS) / 1000 # convert to seconds
                self.events()
                self.update()
                self.draw()
                # 30 coins required to beat the game
                if self.player.moneybag >= 30:
                    self.show_finish_screen()
                    # allow player to play again from level 1
                    self.load_data('./maps/map3.txt')
                    self.new()
                    self.run()
                if self.player.dead:
                    self.show_end_screen()
                    # re-draw map and all sprites
                    self.new()
                    self.run_new_stage()


    def quit(self):
        pg.quit() # close pygame
        sys.exit() # kill python program
        
    def update(self):
        self.all_sprites.update()
        self.teleporters # update it separately because it is drawn separately

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE): 
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT)) # create vertical lines
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y)) # create horizontal lines


    def draw_text(self, text, font_name, size, color, x, y):
        font = pg.font.Font(pg.font.match_font(font_name), size) # match argument 2 with a pygame db of fonts
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y) # moves text to coords where argument specifies
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.camera.update()
        self.camera.custom_draw(self.player)
        # if all static enemies are dead, draw the teleporter
        if self.enemy_count == 0 and self.buffed_enemy_count == 0:
            for row, tiles in enumerate(self.map_data): # function - creates tuples of 2 elements, tuple[0] being the index and tuple[1] being the actual element
                for col, tile in enumerate(tiles):
                    if tile == 'T':
                        self.teleporter = Teleporter(self, col, row)
                        self.teleporters.draw(self.screen)

        # display health/money near top corners                
        self.draw_text(str(self.player.lives), "arial", 50, WHITE, 50, 25)
        self.draw_text(str(self.player.moneybag), "arial", 50, WHITE, 975, 30)
        pg.display.flip()

    # get user input
    def events(self):
        keys = pg.key.get_pressed()
        for event in pg.event.get(): # check for user input
            if event.type == pg.QUIT: # press the 'x' and exit application
                self.quit()

        # restart functionality
        if keys[pg.K_r]:
            # reset everything
            self.enemy_count = 0
            self.buffed_enemy_count = 0
            self.player.moneybag = 0
            # restart from lvl 1
            self.load_data('./maps/map3.txt')
            self.new() 
            self.run()

# instantiating the Game class
g = Game()
while True:
    g.new()
    g.run()
