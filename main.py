from pygame import *
import pygame

from typing import Tuple
from random import randint, choice

from time import time

init()
# mixer.init()

# mixer.music.load('sounds/space.ogg')
# mixer.music.play(-1)

FPS = 30
W, H = 500, 700

window = display.set_mode((W, H))
clock = pygame.time.Clock()

bg = transform.scale(
    image.load('images/galaxy.jpg'),
    (W, H)
)

enimy_img = 'images/ufo.png'

enimy_lst = []
bullets = []


class Player(sprite.Sprite):
    def __init__(
        self,
        position: Tuple[int, int],
        size: Tuple[int, int],
        speed,
        bullet_size: Tuple[int, int],
        bullet_img: str,
        img: str
    ):
        super().__init__()
        self.img = transform.scale(
            image.load(
                img
            ), 
            size
        )
        self.speed = speed
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = position
        self.bullet = transform.scale(
            image.load(
                bullet_img
            ), bullet_size
        ) 
        self.spawn_time = time()
        self.interval = 0.8
    
    def move(self, keys) -> None:
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed
        
        if keys[K_LSHIFT]:
            current_time = time()
            if current_time - self.spawn_time >= self.interval:
                bullet_rect = self.bullet.get_rect(center=(self.rect.x + 20, self.rect.y + 35))
                bullets.append(bullet_rect)
                
                self.spawn_time = current_time
            
    def update_bullets(self):
        for bullet in  bullets:
            bullet.y -= 5
            
            for enimy in enimy_lst:
                for bullet in bullets:
                    if bullet.colliderect(enimy.rect):
                        enimy_lst.remove(enimy)
                        bullets.remove(bullet)
    
    
    def draw(self) -> None:
        for bullet in bullets:
            window.blit(self.bullet, bullet)
        window.blit(self.img, (self.rect.x, self.rect.y))


class Enimy(sprite.Sprite):
    def __init__(
        self,
        size: Tuple[int, int],
        speed,
        player: 'Player',
        img: str
    ):
        super().__init__()
        self.img = transform.scale(
            image.load(
                img
            ), size
        )
        self.speed = speed
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = randint(200, 400), randint(10, 50)
        self.player = player
    
    def move(self) -> None:
        self.rect.y += self.speed
    
    def update(self):
        for enimy in enimy_lst:
            if enimy.rect.colliderect(self.player.rect):
                print('Програв')
            enimy.draw()
            enimy.move()
    
    def draw(self) -> None:
        window.blit(self.img, (self.rect.x, self.rect.y))

player = Player((250, 550), (50, 50), 5, (20, 20), 'images/bullet.png','images/rocket.png')

spawn_time = time()
interval = 2

game = True
while game:
    keys = key.get_pressed()
    window.blit(bg, (0, 0))
    
    player.update_bullets()
    player.draw()
    player.move(keys)
    
    currnet_time = time()
    
    if currnet_time - spawn_time >= interval:
        enimy_lst.append(Enimy((30, 40), 2, player, enimy_img))
        
        spawn_time = currnet_time
    
    for enimy in enimy_lst:
        enimy.update()
    
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    display.update()
    clock.tick(FPS)