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
time_delay = 50
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, time_delay)

def game_loop_scene():
    # Game loop
    while not board.end:
        clock.tick(FPS)
        screen.fill(LIGHT_BLACK)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    end_game()
                if event.key == pygame.K_SPACE:
                    board.rotate()
                if event.key == pygame.K_RIGHT:
                    board.move(1, 0)
                if event.key == pygame.K_LEFT:
                    board.move(-1, 0)
            elif event.type == timer_event:
                board.move(0, 1)

        key = pygame.key.get_pressed()       

        # Draw
        board.draw(screen)
        pygame.display.update()
    end_scene()

def end_scene():
    # Game loop
    restart = False
    while not restart:
        clock.tick(FPS)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    end_game()
                if event.key == pygame.K_SPACE:
                    restart = True

        key = pygame.key.get_pressed()       

        # Draw
        # Draw a text using pygame
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Game Over', True, COOL_RED, LIGHT_BLACK)
        textRect = text.get_rect()
        textRect.center = (SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2)
        screen.blit(text, textRect)

        pygame.display.update()
    board.__init__()  # WTF Eric!?
    game_loop_scene()

game_loop_scene()
