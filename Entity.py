import pygame, sys
import random, math

pygame.init()

class Entity(pygame.sprite.Sprite):
    def __init__(self, w, h, states, spritesheet = None):
        pygame.sprite.Sprite.__init__(self)
        self.width = w
        self.height = h
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.spritesheet = spritesheet
        self.flipped = False
        self.state = None
        self.dict_data = states
        
        self.a_timer = 0
        self.a_length = 0
        self.a_speed = 0
        self.interrupt = False
        self.is_animating = False
        self.a_x = 0
        self.scaling = 1
        
        if self.spritesheet == None:
            self.image.fill((255, 0, 0))
        else:
            self.spritesheet = pygame.image.load(spritesheet).convert()
            self.image = self.get_image(0, 0, 1)
    #----------------------------------ANIMATION------------------------------------------
    def get_image(self, row, col, scale):
        #make a new surface and blit spritesheet onto that surface
        image = pygame.Surface((self.width, self.height)).convert_alpha()
        image.blit(self.spritesheet, (0, 0), (col * self.width, row * self.height, self.width, self.height))
        #scale to a given size
        image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        #flip image if facing left
        if(self.flipped):
            image = pygame.transform.flip(image, True, False)
        #render all white as transparent
        image.set_colorkey((0, 255, 0))
        return image
    def a_loop(self):
        if(self.is_animating):
            self.a_timer += self.a_speed
            #base case
            if(self.a_timer >= self.a_length):
                self.is_animating = False
                self.set_state("DEFAULT")
                return
            #get new frame
            self.image = self.get_image(self.a_x, int(self.a_timer), self.scaling)
    #----------------------------------STATE------------------------------------------
    def set_state(self, state):
        #has the state changed (prevents a state from repeatedly resetting itself)
        if(self.check_state(state)):
            self.state = state
            self.a_x = self.dict_data[self.state]["INDEX"]
            self.a_length = self.dict_data[self.state]["FRAME_LEN"]
            self.inter = self.dict_data[self.state]["INTER"]
            
            if not ("SPEED" in self.dict_data[self.state]):
                self.a_speed = 0.15
            else:
                self.a_speed = self.dict_data[self.curState]["SPEED"]
            self.a_timer = 0
            self.is_animating = True
            
    def check_state(self, state):
        #checks if new state is different from current state
        if self.state != state:
            return True
        return False
    def update(self):
        self.a_loop()
    
