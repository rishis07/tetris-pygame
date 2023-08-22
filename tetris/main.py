import pygame
from constants import (
    SCREEN_RESOLUTION,
    FPS,
    WHITE,
    BLACK,
    LIGHT_BLUE,
    LIGHT_BLACK,
    COOL_RED,
)
from assets import World


def end_game():
    pygame.quit()
    quit()


# Init
pygame.init()
screen = pygame.display.set_mode(SCREEN_RESOLUTION)
clock = pygame.time.Clock()
screen_running = True

board = World()

# timer event
counter = 0
time_delay = 200
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, time_delay)

# Game loop
while True:
    clock.tick(FPS)
    screen.fill(LIGHT_BLACK)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                end_game()
            if event.key == pygame.K_r:
                board.rotate()
        elif event.type == timer_event:
            pass
            # board.move(0, 1)

    key = pygame.key.get_pressed()

    if key[pygame.K_DOWN]:
        pass
    if key[pygame.K_UP]:
        pass

    if key[pygame.K_RIGHT]:
        board.move(1, 0)

    if key[pygame.K_LEFT]:
        board.move(-1, 0)

    if key[pygame.K_SPACE]:
        pass

    # Draw
    board.draw(screen)
    pygame.display.update()
