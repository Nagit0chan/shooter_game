from pygame import *
from random import randint
from time import time as timer
FPS = 60
MAX_LOST = 10
GOAL = 25
lost = 0
score = 0
num_fire = 0
rel_time = False
life = 3

win_w = 700
win_h = 500
window = display.set_mode((win_w, win_h))
display.set_caption('Стрэляй!!')
background = transform.scale(image.load('gym.jpg'), (win_w, win_h))

mixer.init()
mixer.music.load('mr_beast.ogg')
mixer.music.set_volume(0.02)
mixer.music.play(-1)

font.init()
font1 = font.SysFont('Arial', 24)
font2 = font.SysFont('Arial', 40)
win = font2.render('УРА! ПОБЕДА!!!', True, (0, 0, 0))
lose = font2.render('провал...', True, (0, 0, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_size):
        super().__init__()
        self.image = transform.scale(image.load(player_image), player_size)
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 610:
            self.rect.x += self.speed
    def fire(self):
        ball = Balls('ball.png', self.rect.centerx - 15, self.rect.top, 10, (30, 30))
        balls.add(ball)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_h:
            self.rect.x = randint(80, win_w - 80)
            self.rect.y = -60
            lost = lost + 1

class Guys(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_h:
            self.rect.x = randint(80, win_w - 80)
            self.rect.y = -60

class Balls(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Player('me.jpg', 305, 430, 7, (60, 60))

terpili = sprite.Group()
for i in range(5):
    teacher = Enemy('gym_teacher.jpg', randint(80, win_w - 80), -60, randint(2, 4), (50, 50))
    terpili.add(teacher)

dangerous = sprite.Group()
for i in range(3):
    chel = Guys('svistunchik.jpg', randint(80, win_w - 80), -60, randint(1, 2), (40, 40))
    dangerous.add(chel)

balls = sprite.Group()

clock = time.Clock()
game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    player.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

            elif e.key == K_KP_ENTER and finish == True:
                score = 0
                lost = 0
                life = 0
                finish = False

    window.blit(background, (0, 0))

    if not finish:
        player.reset()
        player.update()

        terpili.update()
        terpili.draw(window)

        dangerous.update()
        dangerous.draw(window)

        balls.update()
        balls.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time > 0:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(terpili, balls, True, True)

        for c in collides:
            score += 1
            teacher = Enemy('gym_teacher.jpg', randint(80, win_w - 80), -60, randint(1, 5), (50, 50))
            terpili.add(teacher)

        if sprite.spritecollide(player, terpili, True):
            teacher = Enemy('gym_teacher.jpg', randint(80, win_w - 80), -60, randint(2, 4), (50, 50))
            terpili.add(teacher)
            life -= 1

        if sprite.spritecollide(player, dangerous, True):
            chel = Guys('svistunchik.jpg', randint(80, win_w - 80), -60, randint(1, 2), (40, 40))
            dangerous.add(chel)
            life -= 1

        if lost >= MAX_LOST or life == 0:
            finish = True
            window.blit(lose, (200, 200))

        if score >= GOAL:
            finish = True
            window.blit(win, (200, 200))

        text_score = font1.render('Счёт: ' + str(score), 1, (0, 0, 0))
        window.blit(text_score, (10, 10))

        text_lose = font1.render('Пропущено: ' + str(lost), 1, (0, 0, 0))
        window.blit(text_lose, (10, 40))

        text_life = font1.render('Жиза: ' + str(life), 1, (0, 0, 0))
        window.blit(text_life, (600, 10))

    player.reset()

    terpili.draw(window)

    dangerous.draw(window)

    balls.draw(window)

    clock.tick(FPS)
    display.update()