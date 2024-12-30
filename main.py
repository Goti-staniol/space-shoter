from pygame import *
import pygame

from typing import Tuple, Optional
from random import randint, choice

from time import time

init()
mixer.init()

mixer.music.load('sounds/space.ogg')
mixer.music.play(-1)

shot_sound = mixer.Sound('sounds/fire.ogg')

FPS = 30
W, H = 500, 700

window = display.set_mode((W, H))
clock = pygame.time.Clock()

bg = transform.scale(
    image.load('images/galaxy.jpg'),
    (W, H)
)

enemies = []
asteroid_lst = []


class Text(sprite.Sprite):
    def __init__(
        self,
        text: str,
        position: Tuple[int, int],
        size: int,
        color: Tuple[int, int, int],
        font: Optional[str]
    ):
        super().__init__()
        self.position = position
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(text, True, color)
    
    def draw(self):
        window.blit(self.text, self.position)


class D(Text):
    def __init__(self, text, position, size, color, font=None):
        super().__init__(text, position, size, color, font)


class Player(sprite.Sprite):
    def __init__(
        self,
        position: Tuple[int, int],
        size: Tuple[int, int],
        bulets_size: Tuple[int, int],
        speed: int,
        player_img: str,
        bullets_img: str
    ):
        self.player_img = transform.scale(
            surface=image.load(player_img), 
            size=size
        )
        self.bullets = []
        self.rect = self.player_img.get_rect()
        self.rect.x, self.rect.y = position
        self.speed = speed
        self.bullets_speed = 0.8
        self.bullets_img = transform.scale(
            surface=image.load(bullets_img), 
            size=bulets_size
        )
    
    def move(self, keys) -> None:
        if keys[K_d]:
            self.rect.x += self.speed
            
        if keys[K_a]:
            self.rect.x -= self.speed
        
        if keys[K_LSHIFT]:
            shot_sound.play(1)
            self.bullets.append(self.bullets_img.get_rect(
                center=((self.rect.x + 20, self.rect.y + 35))
            ))
    
    def update_bullets(self):
        for bullet in self.bullets:
            for enemy in enemies:
                if enemy.ufo_rect.colliderect(bullet):
                    enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    
            if bullet.y <= 0:
                self.bullets.remove(bullet)
                
            bullet.y -= 9
            
            print(self.bullets)
            
    def draw(self) -> None:
        for bullet in self.bullets:
            window.blit(self.bullets_img, bullet)
            
        window.blit(
            source=self.player_img,
            dest=(self.rect.x, self.rect.y)
        )


class Enemy(sprite.Sprite):
    def __init__(
        self,
        ufo_size: Tuple[int, int],
        asteroid_size: Tuple[int, int],
        speed: int,
        ufo_img: str,
        asteroid_img: str,
        player: 'Player'
    ):
        self.ufo_img = transform.scale(
            surface=image.load(ufo_img),
            size=ufo_size
        )
        self.ufo_rect = self.ufo_img.get_rect()
        self.ufo_rect.x = randint(100, 400)  
        self.ufo_rect.y = randint(80, 100)
        
        self.asteroid_img = transform.scale(
            surface=image.load(asteroid_img),
            size=asteroid_size
        )
        self.asteroid_rect = self.asteroid_img.get_rect()
        self.asteroid_rect.x = randint(100, 400)  
        self.asteroid_rect.y = randint(80, 100)
        
        self.player_rect = player.rect
        
        self.speed = speed
    
    def update(self):
        if self.asteroid_rect.colliderect(self.player_rect) or (
            self.ufo_rect.colliderect(self.player_rect)
        ):
            print('ты проиграл')
        
    def move(self):
        self.asteroid_rect.y += self.speed
        self.ufo_rect.y += self.speed
    
    def draw(self):
        window.blit(self.ufo_img, (self.ufo_rect.x, self.ufo_rect.y))
        window.blit(self.asteroid_img, (self.asteroid_rect.x, self.asteroid_rect.y))
    
timer = 0

player = Player(
    position=(250, 500),
    size=(50, 100),
    bulets_size=(10, 10),
    speed=8,
    player_img='images/rocket.png',
    bullets_img='images/bullet.png'
)



game = True
while game:
    keys = key.get_pressed()
    window.blit(bg, (0, 0))
    
    player.update_bullets()
    player.draw()
    player.move(keys)
    
    timer += 1
    if timer >= 30:
        enemies.append(
            Enemy(
                ufo_size=(50, 50),
                asteroid_size=(50, 50),
                speed=3,
                ufo_img='images/ufo.png',
                asteroid_img='images/asteroid.png',
                player=player
            )
        )
        timer = 0
    
    for enemy in enemies:
        if not enemy.asteroid_rect.colliderect(
            enemy.ufo_rect
        ):
            enemy.update()
            enemy.draw()
            enemy.move()
            
            
            
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    display.update()
    clock.tick(FPS)