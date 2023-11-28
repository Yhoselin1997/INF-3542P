
import random
import numpy
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

NB_AGENTE = 5  # A, B, C, D, E

matriz = numpy.array([
    [0, 7, 8, 10, 15],
    [7, 0, 9, 11, 17],
    [8, 9, 0, 10, 18],
    [10, 11, 20, 0, 5],
    [15, 17, 18, 5, 0]
])

def evalAgente(individual):
    suma = 0
    for i in range(len(individual) - 1):
        suma += matriz[individual[i], individual[i + 1]]
    suma += matriz[individual[-1], individual[0]]
    return suma,

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("permutation", random.sample, range(NB_AGENTE), NB_AGENTE)

toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.permutation)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evalAgente)
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=2.0/NB_AGENTE)
toolbox.register("select", tools.selTournament, tournsize=3)

def main(seed=0):
    random.seed(seed)

    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("Avg", numpy.mean)
    stats.register("Std", numpy.std)
    stats.register("Min", numpy.min)
    stats.register("Max", numpy.max)

    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=100, stats=stats,
                        halloffame=hof, verbose=False)

    return pop, stats, hof

if __name__ == "__main__":
    pop, stats, hof = main()

    best_route_indices = hof[0]
    best_route_nodes = [chr(ord('A') + idx) for idx in best_route_indices]

    print("Mejor recorrido encontrado:", best_route_nodes)
    print("Distancia mínima:", hof[0].fitness.values[0])
