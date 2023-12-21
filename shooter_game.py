#Создай собственный Шутер!
from random import randint
from pygame import *
from time import sleep, time as tm

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 

    def reset(self):
         window.blit(self.image, (self.rect.x, self.rect.y))


num_fire = 0
reload = False
time_reload = 0
fire_delay = 0
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            self.fire()

    def fire(self):
        global num_fire, reload, time_reload, bullets, fire_delay
        if num_fire <= 5 and abs(tm() - time_reload) > 0.2:
            num_fire += 1
            reload = False
            fire_delay = tm()

            bullet = Bullet('bullet.png', self.rect.x + 24, self.rect.y, 2)
            bullets.add(bullet)
            s = mixer.Sound('fire.ogg')
            s.play()
        else:
            reload = True
            time_reload = tm()
            num_fire = 0


class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (16, 16))
        self.rect = self.image.get_rect() 
        self.rect.x = player_x
        self.rect.y = player_y
    def update(self):
        self.rect.y -= self.speed
        self.reset()

lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(1, 700 - self.rect.width)
            global lost
            lost += 1
        self.reset()


class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(1, 700 - self.rect.width)
        self.reset()

# ИГРОВАЯ СЦЕНА
window = display.set_mode((700, 500))
bg = transform.scale(image.load('galaxy.jpg'), (700, 500))
# ФОНОВАЯ МУЗЫКА
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

# СПРАЙТЫ
plaeyer = Player('rocket.png', 250, 420, 7)

bullets = sprite.Group()
enemies = sprite.Group()
for i in range(5):
    enemies.add(Enemy('ufo.png', randint(1,600), 0, randint(1,3)))

asteroids = sprite.Group()
for i in range(3):
    asteroids.add(Asteroid('asteroid.png', randint(1,600), 0, randint(1,3)))
# ТЕКСТ
font.init()
font1 = font.SysFont('verdana', 24)


# ИГРОВОЙ ЦИКЛ
clock = time.Clock()
destroeyed = 0
running = True
while running:
    clock.tick(30)
    window.blit(bg, (0,0))
    
    plaeyer.update()
    plaeyer.reset()
    enemies.update()
    asteroids.update()
    bullets.update()
    text_lost = font1.render(f'Пропущено: {lost}', 1, (255, 255, 255))
    window.blit(text_lost, (20, 20))

    text_destr = font1.render(f'Уничтожено: {destroeyed}', 1, (255, 255, 255))
    window.blit(text_destr, (20, 60))
    for e in event.get():
        if e.type == QUIT:
            running = False
    sprite_list2 = sprite.spritecollide(plaeyer, asteroids, False)
    sprite_list = sprite.spritecollide(plaeyer, enemies, False)
    if len(sprite_list) > 0 or lost >= 3 or len(sprite_list2) > 0:
        text_lose = font1.render('You lose', 1, (255, 255, 255))
        window.blit(text_lose, (300, 240))
        display.update()
        sleep(1)
        running = False
    sprite_list = sprite.groupcollide(enemies, bullets, True, True)
    if len(sprite_list) > 0:
        destroeyed += len(sprite_list)
        for enemy in sprite_list:
            enemy.rect.y = 0
            enemy.rect.x = randint(1, 600)
            enemies.add(enemy)
    if destroeyed >= 10:
        text_lose = font1.render('You win!!!', 1, (255, 255, 255))
        window.blit(text_lose, (300, 240))
        display.update()
        sleep(1)
        running = False
    display.update()