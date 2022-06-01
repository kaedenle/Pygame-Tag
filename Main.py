import pygame, sys
import random, math
from Entity import Entity, Player
from Platform import Level, Platform
from FileLookup import find
from Dictionaries.Dictionary2 import STATE_DICT
from Dictionaries.Controls_Dict import CONTROLS_DICT

pygame.init()
WINDOW_WIDTH = 832
WINDOW_HEIGHT = 640
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 25)
size = 16

WHITE=(255,255,255)
BLUE=(0,0,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLACK = (0, 0, 0)
TARGET_FPS = 60

sprites = pygame.sprite.Group()
textGroup = pygame.sprite.Group()
filename = find("SS2(2)(64x64).png")

class Game:
    def __init__(self):
        self.level = Level(0, size)
        self.level.init()
        self.player = Player(64, 64, STATE_DICT, CONTROLS_DICT, filename)
        sprites.add(self.player)
        self.event = None
        
    def events(self):
        self.event = pygame.event.get()
        for e in self.event:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    def update(self, dt):
        self.events()
        self.player.update(dt, self.event)
        self.level.platList.draw(screen)

game = Game()
while True:      
    pygame.display.update()
    dt = clock.tick(60) * .001 * TARGET_FPS
    screen.fill(WHITE)
    sprites.draw(screen)
    game.update(dt)
