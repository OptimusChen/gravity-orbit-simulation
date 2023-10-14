import numpy as np
import random
import pygame
import math

FPS = 60
SCREEN_SIZE = 1000

ASTEROID = 'asteroid'
PLANET = 'planet'
SUN = 'sun'

ratio = 1

# gravitational constant
# m^3 / (kg * s^2)
g = 6.67 * pow(10, -11)

# so it doesn't take 365 actual days to make 1 orbit
# unit: seconds
regular_time_scale = 3.154e+7 / 365

# setup for asteroid belt so it doesn't just look like a glob of grey stuff
# unit: none
asteroid_time_scale = 40

# ratio of pixels to meters
# pixels/m
ratio = 1 / 920000000

class Body:
    # mass = 10^21 * kg 
    # radius = pixels
    # x, y = m
    # dfs = km
    def __init__(self, radius, mass, dfs, color, v):
        self.radius = radius
        self.mass = mass
        self.x = 0
        self.y = -dfs * 1000
        
        self.color = color
        
        # planet/sun
        self.type = PLANET
                                
        # m/s
        self.velocity = v
        
    # m
    def get_distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        
        return math.sqrt(dx**2 + dy**2)
    
    # newtons
    def get_force(self, other):
        return g * (self.mass * other.mass) / self.get_distance(other)**2
    
    def get_center(self):
        return [SCREEN_SIZE / 2 + self.x * ratio, SCREEN_SIZE / 2 + self.y * ratio]
    
    def get_time_scale(self):
        if (self.type == ASTEROID):
            return regular_time_scale * asteroid_time_scale
        
        return regular_time_scale
    
    def isSun(self):
        return self.type == SUN

sun = Body(30, 1.98892 * 10**30, 0, (255, 255, 0), [0, 0])
sun.type = SUN

# radius of earth, just a arbitrary value
RADIUS = 7

bodies = [sun, 
          Body(RADIUS * 0.382, 3.3011e+23, 5.79e+7, (200, 200, 200), [4.787e+4, 0]), # mercury
          Body(RADIUS * 0.949, 4.8675e+24, 1.082e+8, (255, 255, 255), [3.502e+4, 0]), # venus 
          Body(RADIUS, 5.972e+24, 1.496e+8, (0, 0, 255), [2.9783e+4, 0]), # earth
          Body(RADIUS * 0.532, 6.4171e+23, 2.279e+8, (255, 100, 0), [2.4077e+4, 0]) # mars
         ]

# asteroid belt
ASTEROID_COUNT = 6000
avg_dist = 4.04e+8
avg_mass = 9.29e+20

for i in range(ASTEROID_COUNT):
    dist = (avg_dist + random.randint(-2e+7, 2e+7)) * 1000
    v = math.sqrt(g * sun.mass * ((2 / dist) - (1 / dist)))
        
    asteroid = Body(RADIUS * 0.25, random.randint(4.29e+20, avg_mass), dist / 1000, (100, 100, 100), [v + random.randint(-500, 500), 0])
    asteroid.type = ASTEROID
    
    bodies.append(asteroid)

def update_vectors():
    for body1 in bodies:
        acceleration_x = 0
        acceleration_y = 0
        
        interacting = bodies
        
        # asteroids only interact with sun so your pc doesn't explode
        if (body1.type == ASTEROID):
            interacting = [bodies[0]]
        
        for body2 in interacting:
            if (body1 is body2): continue
            
            force = body1.get_force(body2)
                                
            angle = math.atan2(body1.y - body2.y, body1.x - body2.x)
            
            fx = force * math.cos(angle)
            fy = force * math.sin(angle)
            
            acceleration_x += fx / body1.mass
            acceleration_y += fy / body1.mass
                                                
        body1.velocity[0] -= acceleration_x * body1.get_time_scale()
        body1.velocity[1] -= acceleration_y * body1.get_time_scale()
                
    for body in bodies:
        body.x += body.velocity[0] * body.get_time_scale()
        body.y += body.velocity[1] * body.get_time_scale()
        
pygame.init()
    
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
run = True

clock = pygame.time.Clock()

while run:
    for event in pygame.event.get():
        if event.type == pygame.quit:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                
    screen.fill((0, 0, 0))
    
    for body in bodies:
        pygame.draw.circle(screen, body.color, body.get_center(), body.radius)
    
    update_vectors()
    
    if (pygame.time.get_ticks() > 24000):
        asteroid_time_scale = 1
    
    clock.tick(FPS)
        
    pygame.display.flip()