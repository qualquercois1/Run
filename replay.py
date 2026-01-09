import pygame
import neat
import pickle
import os
import random
import config
from classes import Car, Obstacle

# Função para desenhar o background (copiada do main)
def create_background():
    bg = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT)).convert()
    bg.fill(config.DARK_GRAY)
    for x in range(1, config.TRACK_DIVISION):
        x_real = x * config.DIV_POS
        pygame.draw.line(bg, config.BLACK, (x_real, 0), (x_real, config.GAME_HEIGHT))
    return bg

def replay_genome(config_path, genome_path="winner.pkl"):
    # 1. Carregar Configurações e Genoma
    config_neat = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    # Carrega o arquivo salvo pelo pickle
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # Recria a Rede Neural baseada no genoma vencedor
    net = neat.nn.FeedForwardNetwork.create(genome, config_neat)

    # 2. Setup do Pygame
    pygame.init()
    window = pygame.display.set_mode((config.WIN_WIDTH, config.WIN_HEIGHT))
    pygame.display.set_caption("Replay da Melhor IA")
    clock = pygame.time.Clock()
    
    font = pygame.font.SysFont("Arial", 30)

    # 3. Setup do Jogo
    background = create_background()
    game_screen = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT)).convert()
    
    car = Car()
    obstacles = []
    score = 0
    frames = 0
    running = True
    
    # IMPORTANTE: Usar a mesma taxa de spawn do treino
    spawn_rate = int(config.FPS * (config.SPAWN_INTERVAL / 1000))

    while running:
        frames += 1
        
        # --- Eventos (Apenas para fechar a janela) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Lógica do Jogo ---
        if frames % spawn_rate == 0:
            obstacles_pos = random.sample(range(config.TRACK_DIVISION), config.NUM_OBSTACLES)
            for i in obstacles_pos:
                obstacles.append(Obstacle(i))
        
        obstacles = [obs for obs in obstacles if obs.y < config.GAME_HEIGHT]

        # --- A MÁGICA: IA JOGANDO ---
        inputs = car.get_inputs(obstacles)
        output = net.activate(inputs)

        # Tomada de decisão
        if output[0] > 0.5: car.move("LEFT")
        elif output[1] > 0.5: car.move("RIGHT")

        # Movimento e Colisão
        for obs in obstacles:
            obs.move()
            
            # Checagem de colisão simples visual
            if obs.position == car.position and (obs.y + obs.size_y >= car.y and obs.y <= car.y + car.size_y):
                print(f"Bateu! Score Final: {score}")
                running = False # Para o replay se bater

        score += 1

        # --- Desenho ---
        game_screen.blit(background, (0,0))
        
        for obs in obstacles:
            obs.draw(game_screen)
        
        car.draw(game_screen)

        # Desenha na janela principal
        window.fill(config.BLACK)
        window.blit(game_screen, (config.INIT_X, config.INIT_Y))
        
        # Placar
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        window.blit(text, (10, 10))
        
        if score >= 2000:
            break

        pygame.display.flip()
        
        # Aqui usamos o clock.tick para ver em velocidade humana!
        clock.tick(config.FPS)

    pygame.quit()

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    
    # Verifica se o arquivo existe antes de tentar rodar
    if os.path.exists("winner.pkl"):
        replay_genome(config_path, "winner.pkl")
    else:
        print("ERRO: O arquivo 'winner.pkl' não foi encontrado.")
        print("Rode o arquivo de treino primeiro!")