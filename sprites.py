# This file was created by: Anthony Olakangil

# import necessary modules
from settings import *
# import Sprite class
from pygame.sprite import Group, Sprite
import pygame as pg
import time
import math
import random as rand
# Create a player class
class Player(Sprite):
    def __init__(self, game, x, y): # game parameter is the self of the Game class
        self.groups = game.all_sprites, game.player
        Sprite.__init__(self, self.groups)
        self.game = game # allows player to interact and access everything in game class, used in main.py
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x  = x * TILESIZE
        self.y = y * TILESIZE
        self.lives = 1000
        self.moneybag = 0
        self.speed = 1
        self.powerup_time = 0
        self.allowed = False
        self.weapon = False


    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED * self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED * self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED * self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED * self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= math.sqrt(2)/2
            self.vy *= math.sqrt(2)/2

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.width
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def collide_with_enemies(self, kill):
            self.enemy_hit = None
            hits = pg.sprite.spritecollide(self, self.game.enemies, kill)
            if hits:
                if self.weapon:
                    for sprite in self.game.enemies:
                        if sprite == hits[0]:
                            self.enemy_hit = sprite
                            break
                    self.enemy_hit.kill()
                    self.weapon = False
                    self.game.sword.unequip()
                    # self.game.sword.relocate()
                if not self.weapon:
                    self.lives -= 10
                    # print(self.lives)
                    return True

    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
            if str(hits[0].__class__.__name__) == "Powerup":
                self.speed *= 1.3
                self.powerup_time = time.time()
            if str(hits[0].__class__.__name__) == "Teleporter":
                    self.destination_teleporter = None
                    for sprite in self.game.teleporters:
                        if sprite != hits[0]: # find the object of class Teleporter it didn't collide with
                            self.destination_teleporter = sprite
                            break
                    if self.destination_teleporter:
                        # get x,y coords of destination
                        # move it one tile away so you don't get stuck
                        self.teleporter_x = self.destination_teleporter.rect.topleft[0] + 32
                        self.teleporter_y = self.destination_teleporter.rect.topleft[1] + 32
                        self.x, self.y = self.teleporter_x , self.teleporter_y  
                        # get rid of it so we don't have to handle teleporting back
                        self.destination_teleporter.kill() 
            
            if str(hits[0].__class__.__name__) == "Sword":
                self.game.sword.follow_player()
                self.weapon = True
                # self.game.sword.unequip()


                    


    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt 
        # d = rt, so move player to x pos based on rate and how long it took to get there
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.teleporters, False)
        self.collide_with_group(self.game.powerups, True)
        self.collide_with_group(self.game.swords, False)
        if self.speed > 1 and time.time() - self.powerup_time >= 3: # powerup wears off after 3 seconds
            self.speed = 1
        if self.collide_with_enemies(False): # False: don't kill player sprite until health is equal to 0
            if self.lives == 0:
                self.game.player.kill()
                print('you died')
# Create a wall class
class Wall(Sprite):
    # initialize Wall class with same attributes as Player class, different color
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Enemy(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        Sprite.__init__(self, self.groups)
        self.game = game # allows player to interact and access everything in game class, used in main.py
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.x  = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = ENEMY_SPEED, 0

    def collide_with_walls(self):
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x # unecessary? ask cozort

    def update(self):
        self.x += self.vx * self.game.dt 
        # d = rt, so move player to x pos based on rate and how long it took to get there
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls()
        self.rect.y = self.y

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Powerup(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Teleporter(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.teleporters
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Boss(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.boss
        Sprite.__init__(self, self.groups)
        self.game = game # allows player to interact and access everything in game class, used in main.py
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.x  = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = ENEMY_SPEED, 0
        self.lives = 1000
        # self.follow = False

    def follow_player(self, player):
        # Calculate the direction towards the player (forming a vector which represents 
        # distance from boss to player sprite)
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        # Calculate magnitude of this vector
        self.distance = math.hypot(dx, dy)
        # vector / magnitude = 1, scaling it down but keeping same direction 
        # allows for constant speed
        if self.distance == 0:
            raise Exception("you are too close to the boss!") # end game logically instead of DivideByZeroError

        dx /= self.distance
        dy /= self.distance
        # Set the constant speed
        self.vx = dx * ENEMY_SPEED
        self.vy = dy * ENEMY_SPEED

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                    self.vx = 0
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.left - self.rect.width
                    self.vy = 0
                if self.vy < 0:
                    self.y = hits[0].rect.right
                self.vy = 0
                self.rect.y = self.y

    def collide_with_player(self, kill):
        player_group = pg.sprite.GroupSingle(self.game.player)
        hits = pg.sprite.spritecollide(self, player_group, kill)
        if hits:
            if self.game.player.weapon:
                self.lives -= 10
                if self.lives <= 0:
                    self.kill()
            if not self.game.player.weapon:
                self.game.player.lives -= 50
                print(self.game.player.lives)
                if self.game.player.lives <= 0:
                    # reset to 0 if it ever goes negative
                    self.game.player.lives = 0
                    self.game.player.kill()
                    print("you died")
                    self.game.player.weapon = True
                    self.vx, self.vy = 0, 0



    def update(self):
        self.x += self.vx * self.game.dt 
        # d = rt, so move player to x pos based on rate and how long it took to get there
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.follow_player(self.game.player)
        self.collide_with_walls('x')
        self.collide_with_player(False)
        # print(self.lives)
        self.rect.y = self.y



class Sword(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.swords
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((20, TILESIZE))
        # self.image.fill(WHITE)
        # # Draw the sword on the image
        # # color, (x, y, width, height), outline
        # pg.draw.rect(self.image, SILVER, (5, 1, 4, TILESIZE), 0)  # Blade
        # pg.draw.rect(self.image, SILVER, (0, 16, 15, 6), 0)  # Hilt
        
        #  load an image file instead of drawing it
        self.image = pg.image.load("sword2.png").convert_alpha()  # retains transparent bg features
        self.image = pg.transform.scale(self.image, (40, 60))
        # Set the position of the sprite
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def follow_player(self):
        # Calculate the direction towards the player (forming a vector which represents 
        # distance from boss to player sprite)
        # dx = player.rect.centerx - self.rect.centerx
        # dy = player.rect.centery - self.rect.centery

        # # Calculate magnitude of this vector
        # distance = math.hypot(dx, dy)
        # vector / magnitude = 1, scaling it down but keeping same direction 
        # # allows for constant speed
        # dx /= distance
        # dy /= distance

        # set the constant speed
        # self.vx = dx * PLAYER_SPEED
        # self.vy = dy * PLAYER_SPEED

        self.rect.x = self.game.player.rect.x
        self.rect.y = self.game.player.rect.y

    # def collide_with_enemy(self):
    #     self.enemy_hit = None
    #     hits = pg.sprite.spritecollideany(self, self.game.enemies)
    #     if hits:
    #         for sprite in self.game.enemies:
    #             if sprite == hits[0]:
    #                 self.enemy_hit = sprite
    #         self.enemy_hit.kill()
    #         self.game.player.weapon = False
        
    def unequip(self):
        if self.game.player.weapon == False:
            self.relocate()
    
    def relocate(self):
        # Loop until a valid position is found
        while True:
            # Choose a random position within the boundaries of the map

            # self.game.map_data[0] is the first row of map_data
            # subtract 1 bc/o indexing
            randx = rand.randint(0, len(self.game.map_data[0]) - 1)
            # randy accesses the entire map, not just map_data[0] because all of the indices 
            # represent each row, and by extension the height of the map
            randy = rand.randint(0, len(self.game.map_data) - 1)
            
            # Check if the chosen position is empty (no wall or other object)
            # (y, x) instead of (x, y) --> randy is row index, randx is column index
            # still ends up being (horizontal pos, vertical pos)
            if self.game.map_data[randy][randx] == '.':
                # Set the position of the sword to the chosen position
                self.rect.x = randx * TILESIZE
                self.rect.y = randy * TILESIZE
                break  # Exit the loop once a valid position is found
            


        
