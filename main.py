from pygame import *
import pygame

from typing import Tuple, Optional
from abc import abstractmethod

from random import randint

init()

FPS = 30
W, H = 500, 700

mixer.init()
mixer.music.load('sounds/space.ogg')
mixer.music.play(-1)
shot_sound = mixer.Sound('sounds/fire.ogg')

window = display.set_mode((W, H))
clock = time.Clock()

bg = transform.scale(
    image.load('images/galaxy.jpg'),
    (W, H)
)

enemies = []
lives = 3
timer = 0


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
        self.color = color
        self.position = position
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(text, True, color)
    
    def update_text(self, text: str):
        self.text = self.font.render(text, True, self.color)
    
    def draw(self):
        window.blit(self.text, self.position)


class Attempts(Text):
    def __init__(self, text, position, size, color, font=None):
        super().__init__(text, position, size, color, font)
    
    def update_lives(self, lives):
        super().update_text(f'Життя: {lives}')
    
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
        self.position = position
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
    
    def restart(self) -> None:
        self.rect.x, self.rect.y = self.position
        self.bullets.clear()
        
    
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
        img: str
    ):
        super().__init__()
        self.img = transform.scale(
            surface=image.load(img), 
            size=size
        )
        self.rect = self.img.get_rect()
        self.rect.x = randint(100, 400)
        self.rect.y = randint(80, 100)
        self.speed = speed
    
    def move(self):
        self.rect.y += self.speed
    
    @abstractmethod
    def is_destroyabled(self) -> bool:
        pass
    
    def draw(self):
        window.blit(self.img, (self.rect.x, self.rect.y))


class Asteroid(Enemy):
    def __init__(self, size, speed, img):
        super().__init__(size, speed, img)
        self.angle = 0
        self.original_img = self.img
    
    def update(self):
        self.rotate()

    def rotate(self):
        self.angle += 2.5
        if self.angle >= 360:
            self.angle = 0
        
        self.img = transform.rotate(self.original_img, self.angle)
    
    def is_destroyabled(self):
        return False    


class Ufo(Enemy):
    def __init__(self, size, speed, img):
        super().__init__(size, speed, img)
        
    def is_destroyabled(self):
        return True

attempts = Attempts(
    text='Життя: 3',
    position=(1, 10),
    size=25,
    color=(255, 255, 255),
    font='fonts/Bebas_Neue_Cyrillic.ttf'
)

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
    
    attempts.draw()
    attempts.update()
    
    timer += 1
    if timer >= 40:
        foe_class = Ufo if randint(0, 1) else Asteroid
        foe = foe_class(
            size=(50, 50),
            speed=5,
            img=f'images/{foe_class.__name__.lower()}.png'
        )
        
        enemies.append(foe)
        timer = 0
    
    if lives == 0:
        lives = 3
        attempts.update_lives(lives)
        
        enemies.clear()
        player.restart()
    
    for enemy in enemies:
        enemy.draw()
        enemy.move()
        enemy.update() 
        
        if enemy.rect.colliderect(player.rect):
            lives -= 1
            attempts.update_lives(lives)
            enemies.remove(enemy)
             
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    display.update()
    clock.tick(FPS)