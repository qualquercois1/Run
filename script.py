import pygame, sys, random, os

pygame.init()

# CORES
gray = (70,70,70)
dark_gray = (54,54,54)
red = (255,0,0)
black = (0,0,0)

# Variaveis
# tela
win_width, win_height = 1280,720
game_width, game_height = 1040,560
init_x = (win_width-game_width) // 2
init_y = (win_height-game_height) // 2
fps = 30
running = True
track_division = 3 # quantas pistas terão

# setup da janela
window = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Run")

# background
game_screen = pygame.Surface((game_width, game_height)).convert()
game_screen.fill(dark_gray)
div_pos = game_width//track_division
for x in range(1, track_division):
    x_real = x * div_pos
    pygame.draw.line(game_screen, black, (x_real,0), (x_real, game_height))
game_screen = game_screen.convert()


class Car:
    def __init__(self):
        self.position = 1 # 0,1,2...


def run_game():
    global running
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                

        window.fill(black)
        
        clock.tick(fps)
        window.blit(game_screen, (init_x, init_y))
        pygame.display.flip()

    pygame.quit()
    sys.exit()

run_game()