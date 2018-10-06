import pygame
import random
from sprites import *
from settings import *
import os
vec = pygame.math.Vector2
import time


class Game():
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Simon gets dived")
        self.running = False  
        self.player_pos = vec(0,0)  
        self.mob_timer= 0 
        self.score = 0
        self.level = 5000
        self.difficulty = 'easy'
        self.image = pygame.image.load('img/background.png')
        
        
        #setup shot sound                          
    def displayBackground(self):
        self.screen.blit(self.image,(0,0))
        
    
    def new(self):
        #code for when the user starts a new game
        self.load_data()
        self.show_start()
        self.score = 0
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.all_mobs = pygame.sprite.Group()
        self.all_bullets = pygame.sprite.Group()
        self.player = Player(self)
        self.startGame()
    
    def load_data(self):
        sndupperpath = os.path.join("snd", 'uppercut.wav')
        self.uppercutsnd = pygame.mixer.Sound(sndupperpath) 
        shotpath = os.path.join("snd", 'shoot.wav')
        self.shotpathsnd = pygame.mixer.Sound(shotpath) 
        self.shotpathsnd.set_volume(0.2)       
    
    def drawGrid(self):
        
        for x in range(0,WIDTH,GRID_SIZE):
            pygame.draw.line(self.screen,BLACK,(x,0),(x,HEIGHT))
        for y in range(0,HEIGHT,GRID_SIZE):
            pygame.draw.line(self.screen,BLACK,(0,y),(WIDTH,y))
    
    def display_button(self, font, text, size, color, x, y, w ,h):
        
        pygame.draw.rect(self.screen, color,(x,y,w,h))
        self.display_text(font, text, size, BLACK, x+(0.5*w)  ,y+(0.5*h)  ,  False   )
        pygame.display.update()
        self.difficulty = text   
    
    def show_start(self):
        #this is the code for the start of the game
        
        self.screen.fill(LIGHTBLUE)
        
        self.intro = pygame.image.load('img/Simon64.png')                      
        self.screen.blit(self.intro, (WIDTH / 2 - 30, HEIGHT/3))
        self.display_text('freesansbold.ttf', 'SIMON GETS DIVED', 20, BLACK, (WIDTH / 2), (HEIGHT / 2),False)
        self.display_text('freesansbold.ttf', 'Dont be a pussy - select difficulty below', 10, BLACK, (WIDTH / 2) + 20, (HEIGHT / 1.5),False)
        self.display_button('freesansbold.ttf','easy',5,GREEN,WIDTH/3-25,HEIGHT/1.2,100,50)
        self.display_button('freesansbold.ttf','medium',5,BLUE,(WIDTH/3 + (WIDTH/3)/2) -25,HEIGHT/1.2,100,50)
        self.display_button('freesansbold.ttf','fuckoff',5,RED,(WIDTH/3+WIDTH/3)-25,HEIGHT/1.2,100,50)
        
        pygame.display.flip()
        self.waiting()
    
    def waiting(self):
        waiting = True
        
        while(waiting):
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                    quit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                   #now we check for collision
                    locationx = event.pos[0]
                    locationy = event.pos[1]

                    #shit code to see if we collided
                    
                    #easy
                    if locationy > HEIGHT/1.2 and locationy < HEIGHT/1.2 + 50:
                        if locationx > WIDTH/3-25 and locationx < WIDTH/3-25 + 100:
                            print ('playing easy')
                            self.difficulty = 'easy'
                            waiting = False
                    
                    #medium
                   
                        if locationx > ((WIDTH/3 + (WIDTH/3)/2)) -25 and locationx < (WIDTH/3 + (WIDTH/3)/2)-25 + 100:
                            print ('playing medium')
                            self.difficulty = 'medium'
                            waiting = False
                    
                    #hard
                   
                        if locationx > (WIDTH/3+WIDTH/3)-25 and locationx < (WIDTH/3+WIDTH/3)-25 + 100:
                            print ('playing fuckoff')
                            self.difficulty = 'fuckoff'
                            waiting = False
    
    def drawScore(self):
        self.display_text('freesansbold.ttf', 'SLAINFISTS: ' + str(self.score), 5, WHITE, 80, 30,False)

    def display_text(self,font, text, size, color, x, y, whiteout):
        font = pygame.font.Font(font,20)
        surface = font.render(text, True,color)
        surfRect = surface.get_rect()
        surfRect.center = (x, y)
        
        if whiteout:
            self.screen.fill(WHITE)
        
        self.screen.blit(surface, surfRect)

    def update(self):
        self.all_sprites.update()
        
        now = pygame.time.get_ticks()
        
        switcher = {
            'easy':  3000 + random.choice([-1000,-500,0,500,1600, 1000, 1200, 1500, -800]),
            'medium': 1500 + random.choice([-1000,-800,0,-500,-700, -450, -500, 500,-1000]),
            'fuckoff': 1000 + random.choice([-1000,-800,0,-500,-700, -450, -500, 500,-1000])
        }
        
        level = switcher.get(self.difficulty)
        
        if now - self.mob_timer > level:
            self.mob_timer = now
            Mob(self)
            self.uppercutsnd.play()
            
        if self.all_mobs and self.all_bullets:
            self.dict = pygame.sprite.groupcollide(self.all_bullets, self.all_mobs, True, True)
            if self.dict:
                self.score += 1
        #check if im dead
        
        hits = pygame.sprite.spritecollide(self.player, self.all_mobs, pygame.sprite.collide_mask)

        if hits:
            self.running = False
            
        
        #draw the GRID
        

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.running = False
                print ('quit')
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                
                    self.running = False
                    
            if event.type == pygame.MOUSEBUTTONDOWN: 
                locationx = event.pos[0]
                locationy = event.pos[1]
                self.shotpathsnd.play()
                self.player.firebullet(game,vec(locationx,locationy))
                

       
    def draw(self):
        
        self.screen.fill(WHITE)
        #self.drawGrid()
        self.displayBackground()
        self.drawScore()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def gameOver(self):
        self.screen.fill(LIGHTBLUE)
        pygame.mixer.music.fadeout(500)
        self.display_text('freesansbold.ttf', 'FUCK OFF DOOMFIST: Sleepdarts - ' + str(self.score), 5, BLACK, WIDTH/2, HEIGHT/2,False)
        pygame.display.flip()
        time.sleep(2)
        print('we are game over')
        self.new()
        
    
    def startGame(self):
        
        self.running = True
        pygame.mixer.music.load('snd/happy.OGG')
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.2)
        
        
        while self.running:
            self.clock.tick(60)
            self.events()
            
            self.update()
            
            self.draw()
        
        self.gameOver()
#start the main code here
game = Game()
game.new()   
                                    