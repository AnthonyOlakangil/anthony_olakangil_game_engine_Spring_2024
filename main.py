# This file was created by: Anthony Olakangil

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
12. require key for weapon chest?(TODO)
13. do something with coins (TODO)
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
        self.load_data('map.txt')
        self.running = True
        self.enemy_count = 0
        self.buffed_enemy_count = 0
        self.waiting = None
        self.sound = pg.mixer.Sound('themesong.wav') # load some music
 
 
     # load save game data etc
    def load_data(self, file_name):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, file_name), 'rt') as f: # reading map.txt
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
        self.sound.play(INDEFINITELY) # loop forever until window closed
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
        for row, tiles in enumerate(self.map_data): # function - creates tuples of 2 elements, tuple[0] being the index and tuple[1] being the actual element
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row) # create walls where there is a 1
                if tile == 'P':
                    self.player = Player(self, col, row) # initialize player wherever letter P is located on txt file
                if tile == 'E':
                    Enemy(self, col, row)
                    self.enemy_count = 1
                if tile == 'C':
                    Coin(self, col, row)
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
                    self.buffed_enemy_count += 1

    def stage_2(self):
        self.load_data('map2.txt')
        self.new()  

    def show_new_screen(self):
        self.screen.fill(SILVER)
        self.draw_text("Level: INSANE", "impact", 30, BLACK, WIDTH/2, (HEIGHT/2)-140)
        self.draw_text("-all static guards have increased health and damage", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)-110)
        self.draw_text("    -Unlock the teleporter by killing them!", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)-80)
        self.draw_text("-There are multiple mob bosses.", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)-50)
        self.draw_text("    -you need to unlock the chest for a stronger weapon!", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)-20)
        self.draw_text("    -Don't get too close!", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)+10)
        self.draw_text("-Use powerups to speed away", "comicsansms", 30, BLACK, WIDTH/2, (HEIGHT/2)+40)
        self.draw_text("Don't die!", "impact", 30, BLACK, WIDTH/2, (HEIGHT/2)+100)
        self.draw_text("Press any key to start", "couriernew", 30, BLACK, WIDTH/2, (HEIGHT/2)+150)
        pg.display.flip()
        self.wait_for_key()

                    
    def run(self):
        self.show_start_screen()
        self.playing = True
        # if they have clicked to start/restart
        if not self.waiting:
            if not self.boss.dead:
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
                    if self.boss.dead:
                        self.stage_2()
                        self.run_new_stage()



    def run_new_stage(self):
            self.show_new_screen()
            self.playing = True
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
        if self.enemy_count == 0 and self.buffed_enemy_count == 0:
            for row, tiles in enumerate(self.map_data): # function - creates tuples of 2 elements, tuple[0] being the index and tuple[1] being the actual element
                for col, tile in enumerate(tiles):
                    if tile == 'T':
                        self.teleporter = Teleporter(self, col, row)
                        self.teleporters.draw(self.screen)
        # else:
        #     print(f"enemy count is: {self.enemy_count}")

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
