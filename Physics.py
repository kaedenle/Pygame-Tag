import pygame, math
pygame.init()
class Physics:
    def __init__(self, rect, pos = [0, 0]):
        self.rect = rect

        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)
        self.pos = pygame.Vector2(pos[0], pos[1])

        #make these dynamic?
        self.friction = -0.12
        self.air_res = -0.035
        self.speed = 0.85
        self.airspeed = 0.35
        self.gravity = 0.5

        self.grounded = False
    def limit_vel(self, max_vel_x, max_vel_air, max_vel_y):
        #limiters
        if(self.grounded):
            self.vel.x = max(-max_vel_x, min(self.vel.x, max_vel_x))
        else:
            self.vel.x = max(-max_vel_air, min(self.vel.x, max_vel_air))

        #limit fall speed
        #if self.vel.y > max_vel_y: self.vel.y = max_vel_y
        
        #when the vel gets small, set to 0
        if abs(self.vel.x) < 0.01: self.vel.x = 0
    def collision(self, level):
        def get_index(coord):
            return math.floor(coord/level.TILE_SIZE)
        def in_range(value, minimum, maximum):
            if(value >= minimum and value < maximum):
                return True
            return False
        collisions = [False, False, False, False]
        #vel not optimal due to kinematic equation involving adding acceleration
        delta_x = self.pos.x - self.rect.x
        delta_y = self.pos.y - self.rect.y
        if(delta_x != 0):
            #initial pos
            start_x = get_index(self.rect.x + self.rect.width) if delta_x > 0 else get_index(self.rect.x)
            #next pos
            end_x = get_index(self.pos.x + self.rect.width) if delta_x > 0 else get_index(self.pos.x)
            #set to the initial block
            height_start = get_index(self.rect.y - 1)
            height_end = get_index(self.rect.y + self.rect.height - 1)
            count = 1 if delta_x > 0 else -1
            result = math.inf
            
            for col in range(start_x, end_x + count, count):
                if(result != math.inf):
                    break
                for row in range(height_start, height_end + 1):
                    if(in_range(row, 0, len(level.level)) and in_range(col, 0, len(level.level[0])) and level.level[row][col] == 1):
                        result = col
                        break
            if(result != math.inf):
                self.vel.x = 0
                if(delta_x > 0):
                    if(result * level.TILE_SIZE < self.pos.x + self.rect.width):
                        self.pos.x = (result * level.TILE_SIZE) - self.rect.width - 1
                else:
                    if((result * level.TILE_SIZE) + level.TILE_SIZE > self.pos.x):
                        self.pos.x = (result * level.TILE_SIZE) + level.TILE_SIZE
                        
        if(delta_y != 0):
            #initial pos
            start_y = get_index(self.rect.y + self.rect.height) if delta_y > 0 else get_index(self.rect.y)
            #next pos
            end_y = get_index(self.pos.y + self.rect.height) if delta_y > 0 else get_index(self.pos.y)
            #set to the initial block
            width_start = get_index(self.rect.x)
            width_end = get_index(self.rect.x + self.rect.width)
            count = 1 if delta_y > 0 else -1
            result = math.inf
            
            for row in range(start_y, end_y + count, count):
                if(result != math.inf):
                    break
                for col in range(width_start, width_end + 1):
                    if(in_range(row, 0, len(level.level)) and in_range(col, 0, len(level.level[0])) and level.level[row][col] == 1):
                        result = row
                        break
            if(result != math.inf):
                self.vel.y = 0
                if(delta_y > 0):
                    #on floor
                    if(result * level.TILE_SIZE < self.pos.y + self.rect.height):
                        self.pos.y = (result * level.TILE_SIZE) - self.rect.height
                        self.grounded = True
                else:
                    #hit ceiling or not
                    if((result * level.TILE_SIZE) + level.TILE_SIZE > self.pos.y):
                        self.pos.y = (result * level.TILE_SIZE) + level.TILE_SIZE + 1
    def update(self, dt, level, rect):
        #acceleration = acc_old + velocity * friction
        self.acc.x += self.vel.x * (self.friction if self.grounded else self.air_res)
        #velocity = old_vel + acceleration * time
        self.vel += self.acc * dt
        #limit x and y velocity
        self.limit_vel(100, 10, 14)
        #pos = pos_old + vel * time + acc * 0.5 * time^2
        self.pos += (self.vel * dt) + (self.acc * 0.5) * (dt*dt)
        
        self.collision(level)
        #define the floor (change for boundaries)
        """if self.pos.y > 550:
            self.grounded = True
            self.vel.y = 0
            self.pos.y = 550"""
        #set rect to position
        self.rect.topleft = [self.pos.x, self.pos.y]
        new_pos = self.rect.midbottom
        rect.midbottom = (new_pos[0] + 1, new_pos[1] + 3)
        
