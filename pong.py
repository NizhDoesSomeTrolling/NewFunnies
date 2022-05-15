from pygame import *
from random import randint
speed = 2
speed_x = 0
speed_y = 0
score1 = '0'
score2 = '0'
countdown_frames = 240

mixer.init()
font.init()
font = font.SysFont('Arial', 40)
window = display.set_mode((800,600))
display.set_caption('Pong')

player1win = font.render(
    'Победил Игрок 1', True, (255, 255, 255)
)

player2win = font.render(
    'Победил Игрок 2', True, (255, 255, 255)
)


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, speed, h, w, number):
        super().__init__()
        self.h = h
        self.w = w
        self.image = transform.scale(image.load(player_image),(h,w))
        self.rect_x = x
        self.rect_y = y
        self.rect = Rect((self.rect_x, self.rect_y), (h, w))
        self.speed = speed
        self.number = number

    def reset(self):
        window.blit(self.image, (self.rect_x, self.rect_y))

    def update(self):
        self.rect = Rect((self.rect_x, self.rect_y), (self.h, self.w))

class Player(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()
        if self.number == 1:

            if keys_pressed[K_w] and self.rect_y > 1:
                self.rect_y -= self.speed

            if keys_pressed[K_s] and self.rect_y < 460:
                self.rect_y += self.speed
        if self.number == 2:
            if keys_pressed[K_UP] and self.rect_y > 1:
                self.rect_y -= self.speed

            if keys_pressed[K_DOWN] and self.rect_y < 460:
                self.rect_y += self.speed

class Ball(GameSprite):
    def update(self):
        if self.rect_x < 0 or self.rect_x > 800:
            self.kill()
        self.rect = Rect((self.rect_x, self.rect_y), (self.h, self.w))
    def move(self):
        global speed_y
        if self.rect_y < 10:
            
            speed_y = randint(1, 3)
            speed_y = int(speed_y)
        if self.rect_y > 570:
            
            speed_y = randint(-3, -1)
            speed_y = int(speed_y)
        self.rect_x += speed_x
        self.rect_y += speed_y


background = transform.scale(
    image.load('bg.png'),
    (800,600)
)

player1 = Player('racket.png', 70, 300, speed, 30, 150, 1)
player2 = Player('racket.png', 660, 300, speed, 30, 150, 2)
ball = Ball('ball.png', 300, 300, 0, 30, 30, 0)
balls = sprite.Group()
balls.add(ball)
clock = time.Clock()
FPS = 240
whatever = True
finish = False
while whatever:
    if not finish:
        player1score = font.render(
            score1, True, (255,255,255)
        )

        player2score = font.render(
            score2, True, (255,255,255)
        )


        window.blit(background,(0,0))
        for e in event.get():
            if e.type == QUIT:
                whatever = False
        window.blit(player1score, (50, 50))
        window.blit(player2score, (650, 50))
        window.blit(player1.image,(player1.rect_x,player1.rect_y))
        window.blit(player2.image,(player2.rect_x,player2.rect_y))
        window.blit(ball.image,(ball.rect_x, ball.rect_y))
        player1.update()
        player1.move()
        player2.update()
        player2.move()
        ball.update()
        ball.move()
        if sprite.spritecollide(player1, balls, False):
            speed_x = randint(1,3)
            speed_y = int(speed_y)
            while speed_y == 0: 
                speed_y = randint(-3, 3)
                speed_y = int(speed_y)
        if sprite.spritecollide(player2, balls, False):
            speed_x = randint(-3, -1)
            speed_y = int(speed_y)
            while speed_y == 0: 
                speed_y = randint(-3, 3)
                speed_y = int(speed_y)
        if countdown_frames > 0:
            countdown_frames -= 1
            player1.speed = 0
            player2.speed = 0
        if countdown_frames == 0:
            player1.speed = speed
            player2.speed = speed
            speed_x = 1
            speed_y = 0
            countdown_frames -= 1
        if ball.rect_x < 20:
            score2int = int(score2)
            score2int += 1
            score2 = str(score2int)
            ball.rect_x = 300
            ball.rect_y = 300
            countdown_frames = 240
            speed_x = 0
            speed_y = 0
            player1.rect_y = 300
            player2.rect_y = 300
        if ball.rect_x > 750:
            score1int = int(score1)
            score1int += 1
            score1 = str(score1int)
            ball.rect_x = 300
            ball.rect_y = 300
            countdown_frames = 240
            speed_x = 0
            speed_y = 0
            player1.rect_y = 300
            player2.rect_y = 300
        if score1 == '10' or score2 == '10':
            finish = True
    if finish:
        window.blit(background,(0,0))
        for e in event.get():
            if e.type == QUIT:
                whatever = False
        if score2 == '10':
            window.blit(player2win, (250, 230))
        if score1 == '10':
            window.blit(player1win, (250, 230))
    clock.tick(FPS)
    display.update()
        
    