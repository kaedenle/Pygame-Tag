import pygame
import csv
pygame.init()

class Platform(pygame.sprite.Sprite):
    def __init__(self, row, col, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.w = w
        self.h = h
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.col = col
        self.row = row
        self.index_col = col
        self.index_row = row
    def get_image(self, row, col, scale = 1):
        #make a new surface and blit spritesheet onto that surface
        image = pygame.Surface((self.w, self.h)).convert_alpha()
        #image.blit(self.spriteSheet, (0, 0), (y_index * self.w, x_index * self.h, self.w, self.h))
        #scale to a given size
        #print(scale)
        #print(int(y * (self.w/scale)), " ", int(x * (self.h/scale)))
        self.rect.topleft = [int(col * (self.w/scale)), int(row * (self.h/scale))]
        image = pygame.transform.scale(image, (int(self.w/scale), int(self.h/scale)))
        image.fill((0, 0, 0))
        return image
    
class Level:
    def __init__(self, num, TILE_SIZE):
        self.platList = pygame.sprite.Group()
        self.level_num = num
        self.level = []
        #each tile is 'size x size' (default is 16)
        self.TILE_SIZE = TILE_SIZE
    def load_level(self):
        #read from csv file
        level = []
        with open(f'level{self.level_num}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            #index, value (enumerate produces these)
            for row, rows in enumerate(reader):
                level.append([])
                for col, tile in enumerate(rows):
                    level[row].append(int(tile))
        return level
    def save_level(self):
        #write to csv file
        with open(f'level{self.level_num}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in self.level:
                writer.writerow(row)
    def init(self):
        self.level = self.load_level()
        self.create_plats()
    def create_plats(self):
        self.platList.empty()
        for row, rows in enumerate(self.level):
            for col, tile in enumerate(rows):
                if(tile != 0):
                    platform = Platform(row, col, self.TILE_SIZE, self.TILE_SIZE)
                    platform.get_image(row, col, 1)
                    self.platList.add(platform)
