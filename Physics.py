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
        self.air_res = -0.025
        self.speed = 0.85
        self.airspeed = 0.15
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
        #analyze the x
        xStart = get_index(self.rect.x) if self.vel.x < 0 else get_index(self.rect.x + self.rect.width)
        xDest = get_index(self.pos.x) if self.vel.x < 0 else get_index(self.pos.x + self.rect.width)
        #top height index
        height_index = get_index(self.pos.y)
        #how many times to scan at each x index
        count_index = get_index(self.rect.height)
        count = -1 if self.vel.x < 0 else 1
        
        collision = -math.inf if self.vel.x < 0 else math.inf
        for col in range(xStart, xDest + count, count):
            for row in range(height_index, height_index + count_index + 1):
                #checks to make sure row and col are in bounds
                if((col < len(level.level[0]) and col >= 0) and (row < len(level.level[0]) and row >= 0)):
                    if(level.level[row][col] == 1):
                        collision = col
                        break
        if(self.vel.x < 0):
            #moving left
            self.pos.x = max(self.pos.x, (collision * level.TILE_SIZE) + (level.TILE_SIZE) + 1)
        else:
            #moving right
            self.pos.x = min(self.pos.x + self.rect.width, (collision * level.TILE_SIZE) - 1)
            self.pos.x -= self.rect.width
        if(abs(collision) != math.inf):
            self.vel.x = 0

        #analyze the y
        yStart = get_index(self.rect.y) if self.vel.y < 0 else get_index(self.rect.y + self.rect.height)
        yDest = get_index(self.pos.y) if self.vel.y < 0 else get_index(self.pos.y + self.rect.height)
        #top width index
        width_index = get_index(self.pos.x)
        #how many times to scan at each x index
        count_index = get_index(self.rect.width)
        count = -1 if self.vel.y < 0 else 1
        collision = -math.inf if self.vel.y < 0 else math.inf
        for row in range(yStart, yDest + count, count):
            for col in range(width_index, width_index + count_index + 1):
                #checks to make sure row and col are in bounds
                if((col < len(level.level[0]) and col >= 0) and (row < len(level.level[0]) and row >= 0)):
                    if(level.level[row][col] == 1):
                        collision = row
                        break
        if(self.vel.y < 0):
            #rising
            self.pos.y = max(self.pos.y, (collision * level.TILE_SIZE) + (level.TILE_SIZE))
        else:
            #falling
            if(self.pos.y + self.rect.height > collision * level.TILE_SIZE):
                self.grounded = True
            self.pos.y = min(self.pos.y + self.rect.height, (collision * level.TILE_SIZE) - 1)
            self.pos.y -= self.rect.height
        if(abs(collision) != math.inf):
            self.vel.y = 0
            
    def update(self, dt, level):
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
        if self.pos.y > 550:
            self.grounded = True
            self.vel.y = 0
            self.pos.y = 550
        #set rect to position
        self.rect.topleft = [self.pos.x, self.pos.y]
        
