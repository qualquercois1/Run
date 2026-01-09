import neat, os
from classes import Car, Obstacle
import main
import pickle

def eval_genomes(genomes, config):
    # função de fitness

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        
        fitness = main.game_simulation(net)

        genome.fitness = fitness

    
def run_neat(config_path):
    # 1. Carregar Configuração
    config_neat = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    # 2. Criar População
    p = neat.Population(config_neat)

    # 3. Adicionar Relatórios (Opcional, mas bom para ver no terminal)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # 4. RODAR O TREINO
    # AQUI está a mágica. Você passa a função, não os genomas.
    # O NEAT vai chamar 'eval_genomes' 50 vezes (geraçoes).
    winner = p.run(eval_genomes, 50)
    
    print('\nMelhor genoma salvo como winner!')

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    
    # 1. Carregar Config
    config_neat = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    
    p = neat.Population(config_neat)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    # 2. Rodar Treino
    winner = p.run(eval_genomes, 20) # 20 gerações para testar

    # 3. SALVAR O VENCEDOR (IMPORTANTE!)
    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
        print("Genoma vencedor salvo em 'winner.pkl'")