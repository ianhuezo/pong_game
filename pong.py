import pygame, sys
from pygame.locals import *
import random
from time import sleep

#A Game that I created to test out my bluetooth arduino controller with the raspberry pi 'console'
#I didnt implement the random hit feature for the pong game, just a simple follow on the ball
class Ball:

    def __init__(self, surface, color, radius):
        
        self.surface = surface
        self.color = color
        self.radius = radius
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        
        self.dx = 0#change in x
        self.dy = 0#change in y
        self.speedx = 3#how fast ball is going
        self.speedy = 3#how fast ball is going

        #collision detection variables for player
        self.collisiony = False
        self.collisionx = False
        self.collision_paddle = False
    
        #collision detection variables for bot
        self.collision_bot = False
        self.collision_botx = False
        self.collision_boty = False

        #score
        self.player = 0 #score of player
        self.bot = 0 #score of bot
        self.scored = False

        
        pygame.draw.circle(self.surface, self.color, (int(self.x) , int(self.y)), self.radius, 0)

    def move(self, paddle_p1x, paddle_p1y, paddle_botx, paddle_boty):
        #collision possibilities with movements
        self.collision_paddle = paddle_p1x >= self.x-self.dx and (paddle_p1y<= self.y-self.dy and paddle_p1y + 100 >= self.y-self.dy)
        self.collision_bot = paddle_botx <= self.x - self.dx and (paddle_boty <= self.y - self.dy and paddle_boty +  100 >= self.y - self.dy)
        
        if(self.scored == False):
            if(self.y - self.dy >= HEIGHT or self.y-self.dy <= 0 or self.collision_paddle or self.collision_bot):
                self.collisiony = True #collision on
                if(self.collision_paddle == True):
                    self.collisionx = True
                if(self.collision_bot == True):
                    self.collision_botx = True
                if(self.collisiony == True and self.collision_botx == False and self.collisionx == False):
                        pygame.mixer.Sound('sounds/wall_hit.wav').play()
            if(self.y - self.dy >0 and self.y + self.dy <HEIGHT or self.collisiony == True):
                if(self.collisiony == True or self.collisionx == True):
                    self.collisiony = False
                    self.speedy = -self.speedy#boundary collision occurs
                    if(self.collisionx == True):#paddle collision occurs
                        self.collisionx = False
                        self.speedx = -self.speedx
                        self.speedy = -self.speedy
                        pygame.mixer.Sound('sounds/paddle_hit.wav').play()
                        
                    if(self.collision_botx == True):#paddle collision occurs
                        self.collision_botx = False
                        self.speedx = -self.speedx
                        self.speedy = -self.speedy
                        pygame.mixer.Sound('sounds/paddle_hit.wav').play()
                        
                if(self.collisiony == False and self.collisionx == False and self.collision_botx == False):#collision not occured
                    self.dx += self.speedx
                    self.dy += self.speedy
                    
                # where 30 is the threshold win after the paddle for your player
                if(self.x - self.dx < paddle_p1x - 30):
                    self.bot+= 1
                    self.dx = 0
                    self.dy = 0
                    pygame.mixer.Sound('sounds/paddle_miss.wav').play()
                    pygame.time.wait(3000)
                if(self.x - self.dx > paddle_botx ):
                    self.player+= 1
                    self.dx = 0
                    self.dy = 0
                    pygame.mixer.Sound('sounds/paddle_miss.wav').play()
                    pygame.time.wait(3000)
                    
            #paddle collision
            #win condition
            pygame.draw.circle(self.surface, self.color, (int(self.x - self.dx) , int(self.y - self.dy)), self.radius, 0)
    def scored_point(self):
        return {'player': self.player, 'bot': self.bot}
            
 
    def ball_positionx(self):
        return self.x - self.dx

    def ball_positiony(self):
        return self.y - self.dy

class Pong_P1:

    def __init__(self,surface,color,y_pos):

        self.surface = surface
        self.color = color
        self.x = 10
        self.y = HEIGHT/2.7
        self.thick = 20
        self.length = 100
        self.y_pos = y_pos;
        self.dy = 0;
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.thick, self.length))

    def move(self, direction = 'idle'):
        if(direction == 'down'):
            if(self.y + self.dy + self.length < HEIGHT):
               self.dy += 10
            pygame.draw.rect(self.surface, self.color, (self.x, self.y + self.dy, self.thick, self.length))
        elif(direction == 'up'):
            if(self.y + self.dy > 0):
               self.dy -= 10
            pygame.draw.rect(self.surface, self.color, (self.x, self.y + self.dy, self.thick, self.length))
        elif(direction  == 'idle'):
            pygame.draw.rect(self.surface, self.color, (self.x, self.y + self.dy, self.thick, self.length))
            
    def paddle_posx(self):
        return self.x + self.thick + 5

    def paddle_posy(self):
        return self.y+ self.dy
            
        
class Pong_AI:

    def __init__(self,surface,color):

        self.surface = surface
        self.color = color
        self.x = 570
        self.y = HEIGHT/2.7
        self.thick = 20
        self.length = 100
        self.dy = 0
        self.speed = 2

        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.thick, self.length))

    def follow_ball(self, ball_y):
        if(self.y + self.dy +self.length/2<= ball_y):
            if(self.y - self.dy > 0):
                self.dy += self.speed
        if(self.y + self.dy + self.length / 2 >= ball_y):
            if(self.y - self.dy < HEIGHT - self.length):
                self.dy -= self.speed
        pygame.draw.rect(self.surface, self.color, (int(self.x), int(self.y+self.dy), self.thick, self.length))
    def bot_posx(self):
        return WIDTH - self.thick -10
    
    def bot_posy(self):
        return self.dy + self.y
        
################# Initial setup
pygame.init()
pygame.font.init()
pygame.mixer.init()


#Set text font
myfont = pygame.font.SysFont('Comic Sans MS', 15)

#set display
HEIGHT = 400
WIDTH = 600
COLOR = (0 , 0, 0) #Black Color

DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAY.fill(COLOR)

#Create Ball

BALL_COLOR = (255, 255, 255)
BALL_RADIUS = 10
PONG_COLOR = BALL_COLOR
PONG_WIDTH = 10
PONG_HEIGHT = 40
YPOS = 500

clock = pygame.time.Clock()
player1 = Pong_P1(DISPLAY,PONG_COLOR, YPOS)
the_bot = Pong_AI(DISPLAY,PONG_COLOR)
the_ball = Ball(DISPLAY,BALL_COLOR, BALL_RADIUS)
old_k_delay, old_k_interval = pygame.key.get_repeat ()
pygame.key.set_repeat (50, 30)
## game is running
while True:
    Pong_AI(DISPLAY,PONG_COLOR)
    player_positionx = player1.paddle_posx()
    player_positiony = player1.paddle_posy()
    ball_position = the_ball.ball_positiony()
    bot_posx = the_bot.bot_posx()
    bot_posy = the_bot.bot_posy()
    player_score = the_ball.scored_point()
    p1_score = myfont.render('PLAYER SCORE: '+str(player_score['player']), False, (255,255,255))
    bot_score = myfont.render('BOT SCORE: '+str(player_score['bot']), False, (255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type ==  KEYDOWN:#some key has been pressed, not necessarily down arrow lol
                if(event.key == K_DOWN):
                    player1.move('down')
                elif(event.key == K_UP):
                    player1.move('up')
    DISPLAY.fill(COLOR)
    DISPLAY.blit(p1_score,(WIDTH/5 , 0))
    DISPLAY.blit(bot_score,(0.6* WIDTH  , 0))
    pygame.draw.rect(DISPLAY, (255,255,255), (WIDTH/2, 0, 10, WIDTH))
    the_ball.move(player_positionx, player_positiony,bot_posx, bot_posy)
    the_bot.follow_ball(ball_position)
    player1.move()
    clock.tick(50)
    pygame.display.flip()
pygame.key.set_repeat (old_k_delay, old_k_interval)
