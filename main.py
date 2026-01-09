import pygame
import sys
import random
import os

import config, train
from classes import Car, Obstacle


# Inicialização
window = pygame.display.set_mode((config.WIN_WIDTH, config.WIN_HEIGHT))
pygame.display.set_caption("Run")
clock = pygame.time.Clock()

# Background
def create_background():
    bg = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT)).convert()
    bg.fill(config.DARK_GRAY)
    for x in range(1, config.TRACK_DIVISION):
        x_real = x * config.DIV_POS
        pygame.draw.line(bg, config.BLACK, (x_real, 0), (x_real, config.GAME_HEIGHT))
    return bg

game_screen = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT)).convert()
background = create_background()

# Controle de inputs
def event_inputs(car, running_state):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d: 
                car.move("RIGHT")
            if event.key == pygame.K_a: 
                car.move("LEFT")
    return running_state

# Verificação de colisão
def car_collision(car, obstacles):
    for obs in obstacles:
        if obs.position == car.position and (obs.y+obs.size_y >= car.y and obs.y <= car.y+car.size_y):
            return False
        
    return True

# Função Principal
def run_game():
    running = True
    car = Car()
    obstacles = []
    
    obstacle_spawn_timer = pygame.time.get_ticks()

    while running:
        current_time = pygame.time.get_ticks()
        
        running = event_inputs(car, running) 

        if current_time - obstacle_spawn_timer >= config.SPAWN_INTERVAL:
            obstacles_pos = random.sample(range(config.TRACK_DIVISION), config.NUM_OBSTACLES)
            for i in obstacles_pos:
                obstacles.append(Obstacle(i))
            obstacle_spawn_timer = current_time
            
        obstacles = [obs for obs in obstacles if obs.y < config.GAME_HEIGHT]

        # Desenho
        game_screen.blit(background, (0,0))

        for obs in obstacles:
            obs.move()
            obs.draw(game_screen)

        car.draw(game_screen)

        # Morte
        running = car_collision(car,obstacles)

        inputs = car.get_inputs(obstacles)
        print(f"Esq: {inputs[0]:.2f} | Cen: {inputs[1]:.2f} | Dir: {inputs[2]:.2f}")

        # Blit final na janela
        window.fill(config.BLACK)
        window.blit(game_screen, (config.INIT_X, config.INIT_Y))
        
        pygame.display.flip()
        clock.tick(config.FPS)

    pygame.quit()
    sys.exit()

def game_simulation(net):
    car = Car()
    obstacles = []
    frames = 0
    score = 0
    running = True

    spawn_rate_in_frames = int(config.FPS * (config.SPAWN_INTERVAL / 1000))

    while running:
        # Tempo e Frames
        score += 1
        frames += 1

        # Obstaculos
        if frames % spawn_rate_in_frames == 0:
            obstacles_pos = random.sample(range(config.TRACK_DIVISION), config.NUM_OBSTACLES)
            for i in obstacles_pos:
                obstacles.append(Obstacle(i))
            
        obstacles = [obs for obs in obstacles if obs.y < config.GAME_HEIGHT]

        # Lógica da IA
        inputs = car.get_inputs(obstacles)
        output = net.activate(inputs)

        if output[0] > 0.5: car.move("LEFT")
        elif output[1] > 0.5: car.move("RIGHT")

        for obs in obstacles:
            obs.move()


        if not car_collision(car, obstacles): break

        if score > 2000:
            print("score maximo")
            break

    return score 


