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
    def update(self, dt):
        #acceleration = acc_old + velocity * friction
        self.acc.x += self.vel.x * (self.friction if self.grounded else self.air_res)
        #velocity = old_vel + acceleration * time
        self.vel += self.acc * dt
        #limit x and y velocity
        self.limit_vel(100, 10, 14)
        #pos = pos_old + vel * time + acc * 0.5 * time^2
        self.pos += (self.vel * dt) + (self.acc * 0.5) * (dt*dt)

        #self.collision()
        #define the floor (change for boundaries)
        if self.pos.y > 400:
            self.grounded = True
            self.vel.y = 0
            self.pos.y = 400
        #set rect to position
        self.rect.topleft = [self.pos.x, self.pos.y]
        
