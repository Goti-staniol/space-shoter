import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
PLAYER_COLOR = (255, 0, 0)
PLAYER_SIZE = 50
FPS = 60

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Restart Example")

# Функция для сброса состояния игры
def reset_game():
    global player_pos
    player_pos = [WIDTH // 2, HEIGHT // 2]

# Инициализация игрока
reset_game()

# Основной игровой цикл
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Клавиша "R" для перезапуска
                reset_game()

    # Логика движения (пример)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5
    if keys[pygame.K_UP]:
        player_pos[1] -= 5
    if keys[pygame.K_DOWN]:
        player_pos[1] += 5

    # Отображение игрока
    pygame.draw.rect(screen, PLAYER_COLOR, (*player_pos, PLAYER_SIZE, PLAYER_SIZE))

    # Проверка на поражение (например, выход за границы экрана)
    if player_pos[0] < 0 or player_pos[0] > WIDTH - PLAYER_SIZE or player_pos[1] < 0 or player_pos[1] > HEIGHT - PLAYER_SIZE:
        reset_game()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
