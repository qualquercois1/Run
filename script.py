import pygame, sys, random, os

pygame.init()

# CORES
gray = (70,70,70)
dark_gray = (54,54,54)
red = (255,0,0)
black = (0,0,0)
blue = (0,0,200)

# Variaveis
# tela
win_width, win_height = 1280,720
game_width, game_height = 1040,560
init_x = (win_width-game_width) // 2
init_y = (win_height-game_height) // 2
fps = 30
running = True
track_division = 3 # quantas pistas terão
gap = 5
num_obstacles = 2

# setup da janela
window = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Run")

# background
background = pygame.Surface((game_width, game_height)).convert()
background.fill(dark_gray)
div_pos = game_width//track_division
for x in range(1, track_division):
    x_real = x * div_pos
    pygame.draw.line(background, black, (x_real,0), (x_real, game_height))
game_screen = pygame.Surface((game_width, game_height)).convert()


class Car:
    def __init__(self):
        self.position = track_division // 2
        self.size_x = div_pos-250
        self.size_y = 100
        self.color = red

    def move(self, direction):
        if direction == "RIGHT" and self.position != track_division-1:
            self.position += 1
        elif direction == "LEFT" and self.position:
            self.position -= 1

    def draw(self, surface):
        rect = pygame.Rect(self.position*div_pos+(div_pos-self.size_x)//2, game_height-self.size_y-gap, self.size_x, self.size_y)
        pygame.draw.rect(surface, self.color, rect, border_radius=4)

class Obstacle:
    def __init__(self, position):
        self.y = 0
        self.size_x = div_pos-150
        self.size_y = 100
        self.color = blue
        self.velocity = 3
        self.position = position

    def draw(self, surface):
        rect = pygame.Rect(self.position*div_pos+(div_pos-self.size_x)//2, self.y, self.size_x, self.size_y)
        pygame.draw.rect(surface, self.color, rect, border_radius=4)

    def move(self):
        self.y += self.velocity



def run_game():
    global running
    car = Car()
    obstacles = []
    for i in range(0, num_obstacles):
        obstacle = Obstacle(random.randint(0,track_division-1))
        obstacles.append(obstacle)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d: 
                    car.move("RIGHT")
                if event.key == pygame.K_a: 
                    car.move("LEFT")

        game_screen.blit(background, (0,0)) # desenha o background
        
        for y in obstacles:
            y.draw(game_screen)
            y.move()

        car.draw(game_screen)

        window.fill(black)
        window.blit(game_screen, (init_x, init_y))
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()

run_game()