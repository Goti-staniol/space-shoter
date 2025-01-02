from pygame import *
import pygame

from typing import Tuple, Optional
from abc import abstractmethod

from random import randint
from time import time

init()

FPS = 30
W, H = 500, 700

mixer.init()
mixer.music.load('sounds/space.ogg')
mixer.music.play(-1)
shot_sound = mixer.Sound('sounds/fire.ogg')

window = display.set_mode((W, H))
clock = pygame.time.Clock()

bg = transform.scale(
    image.load('images/galaxy.jpg'),
    (W, H)
)

enemies = []


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
                if enemy.rect.colliderect(bullet):
                    if enemy.is_destroyabled():
                        enemies.remove(enemy)
                        
                    self.bullets.remove(bullet)
                    
            if bullet.y <= 0:
                self.bullets.remove(bullet)
                
            bullet.y -= 9
            
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
        size: Tuple[int, int],
        speed: int,
        img,
        player: 'Player'
    ):
        super().__init__()
        self.img = transform.scale(
            surface=image.load(img), 
            size=size
        )
        self.rect = self.img.get_rect()
        self.rect.x = randint(100, 400)
        self.rect.y = randint(80, 100)
        self.player = player
        self.speed = speed
    
    def move(self):
        self.rect.y += self.speed
    
    @abstractmethod
    def is_destroyabled(self) -> bool:
        pass
    
    def update(self):
        if self.rect.colliderect(self.player.rect):
            print('lose')
        if self.rect.y > H:
            self.kill()
    
    def draw(self):
        window.blit(self.img, (self.rect.x, self.rect.y))


class Asteroid(Enemy):
    def __init__(self, size, speed, img, player):
        super().__init__(size, speed, img, player)
        self.angle = 0
        self.original_img = self.img
    
    def update(self):
        super().update()
        self.rotate()

    def rotate(self):
        self.angle += 2.5
        
        if self.angle >= 360:
            self.angle = 0
        
        self.img = transform.rotate(self.original_img, self.angle)
    
    def is_destroyabled(self):
        return False    

class Ufo(Enemy):
    def __init__(self, size, speed, img, player):
        super().__init__(size, speed, img, player)
        
    def is_destroyabled(self):
        return True
    
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
    if timer >= 40:
        if randint(0, 1):
            foe = Ufo(
                size=(50, 50),
                speed=5,
                img='images/ufo.png',
                player=player
            )
        else:
            foe = Asteroid(
                size=(50, 50),
                speed=5,
                img='images/asteroid.png',
                player=player
            )
        enemies.append(foe)
        timer = 0
        
    for enemy in enemies:
        enemy.draw()
        enemy.move()
        enemy.update()   
             
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    display.update()
    clock.tick(FPS)