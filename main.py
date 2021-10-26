# ---------------NOTES---------------
# 
# ► 1 radian = 180/math.pi
# 
# ► math.pi / 2 = 90 degrees
# 
# 
# 
# 
# 
# 
# 
# 

import pygame
import random
import math

# PYGAME STUFF -----------------------------------------------------------------------------------------------
pygame.init()
(width, height) = (600, 900)
screen = pygame.display.set_mode((width, height)) # creates pygame screen
pygame.display.set_caption('Ball Physics')
clock = pygame.time.Clock()
bgColor = (10,10,10)

# IMAGES -----------------------------------------------------------------------------------------------------
#ballPic = pygame.image.load("ball.png")

# GAME PHYSICS STUFF -----------------------------------------------------------------------------------------
drag = 0.9999 # how much friction, 0-1 (inversed)
elasticity = 0.1 # how much bounce, 0-1
gravity = (math.pi, 0.1) # (dont touch, how much downwards pull 0-1)

# CLASSES & FUNCTIONS ----------------------------------------------------------------------------------------
def addVectors(x, y, angle1, length1, length11, angle2, length2): # helpful function that adds 2 vectors together
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length11 + math.cos(angle2) * length2
    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return (angle, length, length)

def findBall(particles, x, y): # checks if the mouse is clicking the ball
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size: # check if mouseX and mouseY are within the balls area
            return p
    return None

def collide(p1, p2): # prints when the balls collide with each other
    dx = p1.x - p2.x # find x dist
    dy = p1.y - p2.y # find y dist
    
    distance = math.hypot(abs(dx), abs(dy)) # get hypot of those distance values (diagonal)
    if distance < p1.size + p2.size: # check if ball distance is less than their size (they overlap)
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent

        angle1 = 2*tangent - p1.angle # get new angles
        angle2 = 2*tangent - p2.angle # get new angles
        xspeed1 = p2.xspeed*elasticity # get new speeds
        yspeed1 = p2.yspeed*elasticity # get new speeds
        xspeed2 = p1.xspeed*elasticity # get new speeds
        yspeed2 = p1.yspeed*elasticity # get new speeds

        (p1.angle, p1.xspeed, p1.yspeed) = (angle1, xspeed1, yspeed1) # trade values between balls
        (p2.angle, p2.xspeed, p2.yspeed) = (angle2, xspeed2, yspeed2) # trade values between balls

        p1.x += math.sin(angle)*1.5
        p1.y -= math.cos(angle)*1.5
        p2.x -= math.sin(angle)*1.5
        p2.y += math.cos(angle)*1.5

class particle: # BALL OBJECT CLASS --------------------------------------------------------------------------
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (255,0,255)
        self.thickness = 1
        self.xspeed = 0.08
        self.yspeed = 0.02
        self.angle = math.pi / 2
        
        
    def bounce(self): # bounces the ball off the screen borders
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle
            self.xspeed *= elasticity
        elif self.x < self.size: # x collisions 
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.xspeed *= elasticity

        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.yspeed *= elasticity
        elif self.y < self.size: # y collisions 
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.yspeed *= elasticity
            
    
    def move(self): # moves the ball based on angle & speed
        (self.angle, self.xspeed, self.yspeed) = addVectors(self.x, self.y, self.angle, self.xspeed, self.yspeed, gravity[0], gravity[1])
        self.x += math.sin(self.angle) * self.xspeed
        self.y -= math.cos(self.angle) * self.yspeed
        self.xspeed *= drag
        self.yspeed *= drag
    
    
    def draw(self): # draws the ball
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, self.thickness)
        

      
# CREATE A SET AMOUNT OF BALLS ----------------------------------------------------------------------------------
ballCount = 2 # total number of balls on screen
ballList = [] # creates empty ball list

for n in range(ballCount): # makes a number of balls based on ballCount
    size = 16
    x = random.randint(size, width-size)
    y = random.randint(size, height-size)
    ball = particle(x, y, size)
    ball.xspeed = random.random()*10
    ball.yspeed = random.random()*10
    ball.angle = random.uniform(0, math.pi*2)
    ballList.append(ball)

selected_particle = None
running = True # controls if program is running or not
while running: # GAME LOOP -----------------------------------------------------------------------------------
    
    selected_ball = None
    clock.tick(30) # frame rate
    # LOGIC --------------------------------------------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # allows user to close the window
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN: # checks for clicking down on a ball
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = findBall(ballList, mouseX, mouseY)
            if selected_particle:
                selected_particle.color = (0,255,0)
        elif event.type == pygame.MOUSEBUTTONUP: # releases the clicked ball and fixes the color
            if selected_particle != None:
                selected_particle.color = (255,0,255)
            selected_particle = None
    
    if selected_particle: # makes the clicked and held ball follow the mouse
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = math.atan2(dy, dx) + 0.5*math.pi
        selected_particle.xspeed = math.hypot(dx, dy) * 0.1
        selected_particle.yspeed = math.hypot(dx, dy) * 0.1
    
    # RENDER -------------------------------------------------------------------------------------------------
    screen.fill(bgColor)
    
    for i, ball in enumerate(ballList):
        ball.move() # updates all ball movements
        ball.bounce() # bounces the balls off the screen edges
        for ball2 in ballList[i+1:]:
            collide(ball, ball2) # checks for colission between balls
        ball.draw() # draws all balls in the ball list
    
    pygame.display.flip()

# END OF GAME LOOP -------------------------------------------------------------------------------------------
pygame.quit()

