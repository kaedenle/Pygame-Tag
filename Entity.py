import pygame, sys
import random, math
from Physics import Physics

pygame.init()

class Entity(pygame.sprite.Sprite):
    def __init__(self, w, h, states, spritesheet = None):
        pygame.sprite.Sprite.__init__(self)
        self.width = w
        self.height = h
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.spritesheet = spritesheet

        self.moving = False
        self.locked = False
        self.flipped = False
        self.state = None
        self.interrupt = False
        #checks if state is different from last self.update_state call
        self.queued_state = None
        self.dict_data = states
        
        self.a_timer = 0
        self.a_length = 0
        self.a_speed = 0
        self.a_loop = False
        self.is_animating = False
        self.a_x = 0
        self.scaling = 1
        self.physics = Physics(self.rect, [50, 50])
        
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
    def update_animation(self):
        if(self.is_animating):
            self.a_timer += self.a_speed
            #base case
            if(self.a_timer >= self.a_length):
                self.is_animating = False
                if(self.a_loop):
                    self.is_animating = True
                    self.a_timer = 0
                return
            #get new frame
            self.image = self.get_image(self.a_x, int(self.a_timer), self.scaling)
    #----------------------------------STATE------------------------------------------
    def update_state(self):
        #has the state changed (prevents a state from repeatedly resetting itself)
        if(self.queued_state != self.state):
            self.state = self.queued_state
            self.a_x = self.dict_data[self.state]["INDEX"]
            self.a_length = self.dict_data[self.state]["FRAME_LEN"]
            self.interrupt = self.dict_data[self.state]["INTER"]
            self.a_timer = 0
            self.is_animating = True
            
            if not ("SPEED" in self.dict_data[self.state]):
                self.a_speed = 0.15
            else:
                self.a_speed = self.dict_data[self.state]["SPEED"]
            #Possibaly implement if loop is true then interrupt must be true
            if not ("LOOP" in self.dict_data[self.state]):
                self.a_loop = False
            else:
                self.a_loop = self.dict_data[self.state]["LOOP"]
                
            if not ("LOCK" in self.dict_data[self.state]):
                self.locked = True
            else:
                self.locked = self.dict_data[self.state]["LOCK"]
                
        if(self.state == None):
            return
        #run the state function
        if("FUNCT" in self.dict_data[self.state]):
            self.dict_data[self.state]["FUNCT"](self)
    def set_state(self, state):
        #check if allowed to change state
        if(self.is_animating == False or self.interrupt == True):
            self.queued_state = state
            return True
        #check if whitelist exists for state
        if("WL" in self.dict_data[self.state]):
            #change if state in whitelist and allowed to change state
            if(state in self.dict_data[self.state]["WL"] and (self.is_animating == False or self.interrupt == True)):
                self.queued_state = state
                return True
        #check if blacklist exists for state
        if("BL" in self.dict_data[self.state]):
            #change if state in blacklist
            if(state in self.dict_data[self.state]["BL"]):
                return False
        return False
            
    def update(self, dt):
        self.a_loop()
        self.physics.update(dt)

class Player(Entity):
    def __init__(self, w, h, states, controls, spritesheet = None):
        Entity.__init__(self, w, h, states, spritesheet)
        self.controls = controls
    def default_state(self):
        #will add differnt set_states for airborne players
        if(self.physics.grounded):
            self.set_state("DEFAULT")
        self.moving = False
    def run(self):
        speed = self.physics.speed if self.physics.grounded else self.physics.airspeed
        if(self.flipped):
            self.physics.acc.x -= speed
        else:
            self.physics.acc.x += speed
    def jump(self):
        if(self.a_timer == 0):
            self.physics.acc.y = -10.5
            self.physics.grounded = False
        if(self.moving):
            self.run()
    def events(self, event):
        self.default_state()
        #physics values
        self.physics.acc.x = 0
        self.physics.acc.y = self.physics.gravity
        
        #hold events
        keys = pygame.key.get_pressed()
        if keys[self.controls["MOVE_RIGHT"]]:
            self.set_state("RUN")
            if not self.locked:
                self.flipped = False
                self.moving = True
        elif keys[self.controls["MOVE_LEFT"]]:
            self.set_state("RUN")
            if not self.locked:
                self.flipped = True
                self.moving = True
        #single press events
        for e in event:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_w and self.physics.grounded:
                    self.set_state("JUMP")
                if e.key == pygame.K_SPACE:
                    self.set_state("SWING")
    def update(self, dt, event):
        self.update_animation()
        self.events(event)
        self.update_state()
        self.physics.update(dt)
