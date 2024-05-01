# This file was created by: Anthony Olakangil

# import necessary modules
from settings import *
# import Sprite class
from pygame.sprite import Sprite
import pygame as pg
import time
import math
import random as rand
from os import path

dir = path.dirname(__file__)
img_dir = path.join(dir, 'static')

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        # image = pg.transform.scale(image, (width * 4, height * 4))
        return image
    
# Create a player class
class Player(Sprite):
    def __init__(self, game, x, y): # game parameter is the self of the Game class
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.jumping = False
        self.walking = False
        self.current_frame = 0
        self.last_update = 0
        self.groups = game.all_sprites, game.player_group
        Sprite.__init__(self, self.groups)
        self.game = game # allows player to interact and access everything in game class, used in main.py
        self.vx, self.vy = 0, 0
        self.x  = x * TILESIZE
        self.y = y * TILESIZE
        self.lives = 1000
        self.moneybag = 0
        self.speed = 1
        self.powerup_time = 0
        self.weapon_basic = False
        self.weapon_big = False
        self.dead = False
        # self.unlock_time = 0
        self.check_if_collided_once = 0
        # probably need a better variable name
        self.collided_once2 = 0
        self.magnet = False
        self.magnet_time = 0

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32),
                                self.spritesheet.get_image(32, 0, 32, 32)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.spritesheet.get_image(678, 860, 120, 201),
                              self.spritesheet.get_image(692, 1458, 120, 207)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.spritesheet.get_image(256, 0, 128, 128)
        self.jump_frame.set_colorkey(BLACK)

    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.walking:
            if now - self.last_update > 500:
                self.last_update = now
                # seamless looping (adding 1 would make 2 % 2 = 0, switching the frame back to the 0th standing frame)
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if self.jumping:
            bottom = self.rect.bottom
            self.image = self.jump_frame
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    # wait for user input from wasd or arrow keys to move
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
        # make movement more free; not tile based
        if self.vx != 0 and self.vy != 0:
            self.vx *= math.sqrt(2)/2
            self.vy *= math.sqrt(2)/2

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0: # collision from the left
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right # collision from the right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.width # collision from top
                if self.vy < 0:
                    self.y = hits[0].rect.bottom # collision from bottom
                self.vy = 0
                self.rect.y = self.y

    def collide_with_enemies(self, kill):
            self.enemy_hit = None
            hits = pg.sprite.spritecollide(self, self.game.enemies, kill)
            if hits:
                if self.weapon_basic or self.weapon_big:
                    for sprite in self.game.enemies:
                        # determine which enemy in the group player collided with
                        if sprite == hits[0]:
                            self.enemy_hit = sprite
                            break

                    self.enemy_hit.kill()
                    self.game.enemy_count -= 1
                    self.weapon_basic = False
                    # drop basic sword after each collision
                    self.game.basic_sword.unequip()

                if not self.weapon_big and not self.weapon_basic:
                    # without a sword, lose hitpoints
                    self.lives -= 10
                    return True
    
    def collide_with_buffed_enemies(self, kill):
            self.buffed_enemy_hit = None
            hits = pg.sprite.spritecollide(self, self.game.buffed_enemies, kill)
            if hits:
                if self.weapon_basic or self.weapon_big:
                    # determine which sprite in the group was collided with
                    for sprite in self.game.buffed_enemies:
                        if sprite == hits[0]:
                            self.buffed_enemy_hit = sprite
                            break
                    if self.weapon_basic:
                        self.buffed_enemy_hit.lives -= 10
                        if self.buffed_enemy_hit.lives == 0:
                            self.buffed_enemy_hit.kill()
                            self.game.buffed_enemy_count -= 1
                            self.weapon_basic = False
                            self.game.basic_sword.unequip()

                    elif self.weapon_big:
                        # big sword does more damage, equipped permanently
                        self.buffed_enemy_hit.lives -= 100
                        if self.buffed_enemy_hit.lives == 0:
                            self.buffed_enemy_hit.kill()
                            self.game.buffed_enemy_count -= 1
                else:
                    self.lives -= 20
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
                        # determine which of the 2 sprites was NOT collided with
                        if sprite != hits[0]: # find the object of class Teleporter it didn't collide with
                            self.destination_teleporter = sprite
                            break
                    if self.destination_teleporter:
                        # get x,y coords of destination
                        # move 1 tile left 2 tiles down of teleporter so player doesn't get stuck
                        self.teleporter_x = self.destination_teleporter.rect.topleft[0] - 32
                        self.teleporter_y = self.destination_teleporter.rect.topleft[1] + 64
                        self.x, self.y = self.teleporter_x , self.teleporter_y  
                        self.teleported = True

            if str(hits[0].__class__.__name__) == "Basic_sword":
                self.game.basic_sword.follow_player()
                self.weapon_basic = True

            if str(hits[0].__class__.__name__) == "Excalibur":
                self.game.player.basic_sword = False # make sure it's not still "equipped"
                self.game.big_sword.ready = False
                # only track time of the first collision
                self.check_if_collided_once += 1
                self.game.big_sword.unlock() # keeps checking if player has unlocked the chest; if they have, render sword image
                self.game.basic_sword.kill() # no need for a worse weapon!
                # self.game.big_sword.follow_player()
                self.weapon_big = True
                return True
            if str(hits[0].__class__.__name__) == "Magnet":
                # print('hit')
                self.magnet = True
                # only start counting once, after the first collision
                self.collided_once2 += 1
                # constantly check if 5 seconds has passed
                self.game.magnet.unequip()
                self.game.magnet.follow_player()
                # iterate through all sprites in coins group to do the same thing  
                for coin in self.game.coins:
                    if not self.game.magnet.alive():  # Check if magnet is still alive
                        coin.vx, coin.vy = 0, 0
                        break  # Exit the loop if magnet is dead
                    coin.following = True
                

    def update(self):
        self.animate()
        self.get_keys()
        self.x += self.vx * self.game.dt 
        # d = rt, so move player to pos based on rate and how long it takes to get there (based on FPS)
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.teleporters, False)
        self.collide_with_group([self.game.big_sword], False) # make it an iterable to avoid error
        self.collide_with_group(self.game.powerups, True)
        self.collide_with_group(self.game.magnets, False)

        if self.speed > 1 and time.time() - self.powerup_time >= 3: # powerup wears off after 3 seconds
            self.speed = 1

        self.collide_with_group(self.game.swords, False)

        if self.collide_with_enemies(False): # False: don't kill player sprite until health is equal to 0
            if self.lives == 0:
                self.kill()
                self.dead = True
                print('you died')

        if self.collide_with_buffed_enemies(False):
            if self.lives == 0:
                self.kill()
                self.dead = True
                print('you died')

# Create a wall class
class Wall(Sprite):
    # initialize Wall class with same attributes as Player class, different color
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
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
        self.image = pg.image.load("./static/enemy.png").convert_alpha()  # retains transparent bg features and pixel format
        self.image = pg.transform.scale(self.image, (40, 60)) # scale it down
        # Set the position of the sprite
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.x  = x * TILESIZE
        self.y = y * TILESIZE
        self.lives = 1
        # only move back and forth (x direction)
        self.vx, self.vy = ENEMY_SPEED, 0

    def collide_with_walls(self):
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                # go back and forth 
                self.vx *= -1
                self.rect.x = self.x

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
        self.image = pg.image.load("./static/coin_animation.gif").convert_alpha()
        self.image = pg.transform.scale(self.image, (30, 30)) # scale it down
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.vx, self.vy = 0, 0
        self.following = False

    # getter
    def get_pos(self):
        return (self.rect.x, self.rect.y)
    
    def follow_player(self, player):
        # Calculate the direction towards the player (forming a vector which represents 
        # distance from coin to player sprite)
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        # Calculate magnitude of this vector
        self.distance = math.hypot(dx, dy)

        if self.distance == 0:
            pass
        
        # vector / magnitude = 1, scaling it down but keeping same direction 
        # allows for constant speed
        dx /= self.distance
        dy /= self.distance
        # Set the constant speed
        self.vx = dx * MAGNET_ATTRACTION
        self.vy = dy * MAGNET_ATTRACTION

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

    def update(self):
        # constantly force resetting pos to deal with 0,0 respawn bug
        self.x = self.get_pos()[0]
        self.y = self.get_pos()[1]
        self.x += self.vx * self.game.dt 
        # d = rt, so move player to x pos based on rate and how long it took to get there
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        if self.following:
            # print(self.following)
            self.follow_player(self.game.player)
      

class Powerup(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("./static/speed.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (60, 60)) # scale it down
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
        self.image = pg.image.load("./static/teleporter.jpg").convert_alpha()  # retains transparent bg features
        self.image = pg.transform.scale(self.image, (40, 60)) # scale it down
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Boss(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.boss_group
        Sprite.__init__(self, self.groups)
        self.game = game # allows player to interact and access everything in game class, used in main.py
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.x  = x * TILESIZE
        self.y = y * TILESIZE
        # initialize velocity as 0
        self.vx, self.vy = 0, 0
        # 1 million lives - make it impractical to kill boss without a weapon upgrade
        self.dead = False
        self.lives = 1000000

    def follow_player(self, player):
        # Calculate the direction towards the player (forming a vector which represents 
        # distance from boss to player sprite)
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        # Calculate magnitude of this vector
        self.distance = math.hypot(dx, dy)

        if self.distance == 0:
            raise Exception("you are too close to the boss!") # end game logically instead of DivideByZeroError
        
        # vector / magnitude = 1, scaling it down but keeping same direction 
        # allows for constant speed
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
        player_group = pg.sprite.GroupSingle(self.game.player_group) # GroupSingle to avoid object not iterable error
        hits = pg.sprite.spritecollide(self, player_group, kill)
        if hits:
            if self.game.player.weapon_basic and not self.game.big_sword.ready:
                self.lives -= 10
                print(f"boss lives with basic weapon: {self.lives}")
                if self.lives <= 0:
                    self.dead = True
                    self.kill()
            elif self.game.player.weapon_big and self.game.big_sword.ready:
                self.lives -= 10000
                print(f"boss lives with big weapon: {self.lives}")
                if self.lives <= 0:
                    self.dead = True
                    self.kill()
            if not self.game.player.weapon_basic and not self.game.player.weapon_big:
                self.game.player.lives -= 50
                if self.game.player.lives <= 0:
                    # reset to 0 if it ever goes negative
                    self.game.player.lives = 0
                    self.game.player.kill()
                    self.game.player.dead = True
                    print("you died")
                    self.vx, self.vy = 0, 0\
                    
    def update(self):
        self.x += self.vx * self.game.dt 
        # d = rt, so move player to x pos based on rate and how long it took to get there
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.follow_player(self.game.player)
        # don't check for collision in y dir
        self.collide_with_walls('x')
        self.collide_with_player(False)
        self.rect.y = self.y


class Basic_sword(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.swords
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #  load an image file instead of drawing it
        self.image = pg.image.load("./static/sword2.png").convert_alpha()  # retains transparent bg features
        self.image = pg.transform.scale(self.image, (40, 60))
        # Set the position of the sprite
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def follow_player(self):
        self.rect.x = self.game.player.rect.x
        self.rect.y = self.game.player.rect.y
        
    def unequip(self):
        if self.game.player.weapon_basic == False:
            self.relocate()
    
    def relocate(self):
        # Loop until a valid position is found
        while True:
            # Choose a random position within the boundaries of the map
            # subtract 1 bc/o indexing
            randx = rand.randint(0, len(self.game.map_data) - 1)
            randy = rand.randint(0, len(self.game.map_data) - 1)

            # Check if the chosen position is empty (no wall or other object)
            if self.game.map_data[randx][randy] == '.':
                print(self.game.map_data[randx][randy])
                # Set the position of the sword to the valid position
                self.rect.x = randx * TILESIZE
                self.rect.y = randy * TILESIZE
                break  # Exit the loop once a valid position is found


class Excalibur(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.swords
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game 
        self.image = pg.image.load("./static/chest.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.ready = False
        self.unlock_time = None

    def unlock(self):
        # only track time relative to the first collision detected
        if self.game.player.check_if_collided_once == 1:
            self.unlock_time = time.time()
        if time.time() - self.unlock_time <= 3:
            # same time logic as speed cooldown
            print(f"unlocking: {(((time.time() - self.unlock_time)/3)*100):.2f}%") # print progress of unlocking /3 seconds, 2 decimal places
        elif time.time() - self.unlock_time >= 3:
            if not self.ready:
                self.ready = True

        if self.ready:
            self.image = pg.image.load("./static/rainbowsword.png").convert_alpha()  # retains transparent bg features
            self.image = pg.transform.scale(self.image, (40, 60))
            # Set the position of the sprite
            self.rect = self.image.get_rect()

    def update(self):
        if self.ready:
            # constantly follow player, never gets unequipped
            self.rect.x = self.game.player.rect.x
            self.rect.y = self.game.player.rect.y

class BuffedEnemy(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.buffed_enemies
        Sprite.__init__(self, self.groups)
        self.game = game # allows player to interact and access everything in game class, used in main.py
        self.image = pg.image.load("./static/boss.png").convert_alpha()  # retains transparent bg features
        self.image = pg.transform.scale(self.image, (60, 80))
        # Set the position of the sprite
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.x  = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = ENEMY_SPEED, 0
        # more hitpoints than lvl 1 static
        self.lives = 1000

    # same collision logic as lvl 1 statics
    def collide_with_walls(self):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.vx *= -1
            self.rect.x = self.x 

    def update(self):
        self.x += self.vx * self.game.dt 
        # d = rt, so move player to x pos based on rate and how long it took to get there
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls()
        self.rect.y = self.y

class Magnet(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.magnets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("./static/Magnet.webp").convert_alpha()
        self.image = pg.transform.scale(self.image, (40, 40)) # scale it down
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def follow_player(self):
        # same logic as sword classes 
        self.rect.x = self.game.player.rect.x
        self.rect.y = self.game.player.rect.y


    def unequip(self):
        # player is only given 5 seconds to use the magnet
        # counting starts after the first collision
        if self.game.player.collided_once2 == 1:
            self.game.player.magnet_time = time.time()
            
        if time.time() - self.game.player.magnet_time >= 5:
            for coin in self.game.coins:
                coin.following = False
                print(coin.following)
            self.game.magnet.kill()
            print("magnet cooldown initiated!")
