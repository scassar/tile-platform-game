'''
Created on 3 Oct. 2018

@author: Shaun
'''
import pygame
import random
vec = pygame.math.Vector2
from settings import *
import random
import math

class Player(pygame.sprite.Sprite):
    def __init__(self,game):
        self.groups = game.all_sprites
        self.layers = 1
        self.game = game
        
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.imagenorm = self.image = pygame.image.load('img/Simon64.png')
        self.imageflip = pygame.image.load('img/Simon642.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.image = self.imagenorm
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH /2, HEIGHT/2)
        self.pos = vec(WIDTH /2, HEIGHT/2)
        self.accel = vec(0,0)
        self.vel = vec(0,0)
    
    
    def update(self):
        
        self.accel.x = 0
        self.accel.y = 0
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.accel.x = -PLAYER_SPEED
        if keys[pygame.K_d]:
            self.accel.x = PLAYER_SPEED
        if keys[pygame.K_w]:
            self.accel.y = -PLAYER_SPEED
        if keys[pygame.K_s]:
            self.accel.y = PLAYER_SPEED
        
        self.accel += self.vel * FRICTION  
        self.vel += self.accel
        self.pos += self.vel
        
        if (self.vel.x < 0):
            self.image = self.imageflip
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.image = self.imagenorm
            self.mask = pygame.mask.from_surface(self.image)
            
        
       # print (self.vel)
    #print (self.vel.x)
        
        if (self.pos.x < 0+1 or self.pos.x > WIDTH -1):
            self.vel.x = 0
        if (self.pos.y < 0+1 or self.pos.y > HEIGHT -1):
            self.vel.y = 0
            
        self.rect.center = self.pos
        self.game.player_pos = self.pos
        
       # print ('self' + str(self.rect))
       # print ('mob' + str((self.game.player_pos)))
       
    def firebullet(self,game, location):
        #create a new bullet
        Bullet(self, self.game, location)


class Bullet(pygame.sprite.Sprite):
    def __init__(self,player, game,location):
        self.groups = game.all_sprites, game.all_bullets
        
        self.layers = 2
        self.location = location
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.image = pygame.Surface(BULLETWIDTH)
        self.image.fill(BLACK)        
        self.rect = self.image.get_rect()
        self.pos = vec(player.pos.x, player.pos.y)
        self.rect.center = (player.pos.x, player.pos.y)
        self.accel = BULLETSPEED
        self.vel = vec(0,0)
        self.direction = vec(0,0)
        
        self.determineDirection(self.location)
        
        self.rect.center = self.pos

        
    def update(self):
        #track the bullet in a straight line        
        #self.determineDirection(self.location)
        
        #flip the image if required
        
        
        if self.pos.x < 0 or self.pos.x > WIDTH:
            self.kill()
        if self.pos.y > HEIGHT or self.pos.y < 0:
            self.kill()    
            
        
        self.pos -= self.direction 
        self.rect.center = self.pos 
        
        
    def determineDirection(self,location):
        
        self.dx, self.dy = self.pos.x - location.x, self.pos.y - location.y
        dist = math.hypot(self.dx, self.dy)
        self.dx, self.dy = self.dx / dist, self.dy / dist
        # move along this normalized vector towards the player at current speed
        self.pos.x -= self.dx * self.accel
        self.pos.y -= self.dy * self.accel

        self.direction = vec(self.dx * self.accel, self.dy * self.accel)
       


        
class Mob(pygame.sprite.Sprite):
    def __init__(self,game):
        self.groups = game.all_sprites, game.all_mobs
        self.layers = 1
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.image = pygame.image.load("img/doomfist2.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.pos = vec(random.randrange(0,WIDTH), random.choice((800, 0)))
        self.rect.center = (random.randrange(0,WIDTH), random.choice((800, 0)))
        self.type = DOOMFISTTYPES[0]
        self.vel = self.type
        self.accel = DOOMFISTACCEL
        self.dx = 0
        self.dy = 0
        
        
    def update(self):
        #code to update the doomfist
        self.moveTowardsPlayer(self.game)
        
        self.rect.center = self.pos
    
    def moveTowardsPlayer(self,game):
        
        self.dx, self.dy = self.pos.x - game.player_pos.x, self.pos.y - game.player_pos.y
        dist = math.hypot(self.dx, self.dy)
        self.dx, self.dy = self.dx / dist, self.dy / dist
        # move along this normalized vector towards the player at current speed
        self.pos.x -= self.dx * self.accel
        self.pos.y -= self.dy * self.accel
        
        
        
            