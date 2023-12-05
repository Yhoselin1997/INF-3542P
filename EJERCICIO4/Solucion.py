import random
import numpy as np
from deap import algorithms, base, creator, tools

grafo = np.loadtxt("agente1.csv",delimiter=";")

num_nodos = len(grafo)

nodos = ["A", "B", "C", "D", "E"]

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("indices", random.sample, range(num_nodos), num_nodos)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", lambda ind: (sum(grafo[ind[i - 1]][ind[i]] for i in range(num_nodos)),))

def main(seed=0):
    random.seed(seed)

    pop_size = 100
    num_generaciones = 500
    prob_cruce = 0.7
    prob_mutacion = 0.2

    pop = toolbox.population(n=pop_size)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    stats.register("avg", np.mean)

    algorithms.eaMuPlusLambda(pop, toolbox, mu=pop_size, lambda_=2*pop_size,
                            cxpb=prob_cruce, mutpb=prob_mutacion,
                            ngen=num_generaciones, stats=stats, halloffame=hof, verbose=False)  

    mejor_recorrido = hof[0]
    distancia_total = sum(grafo[mejor_recorrido[i - 1]][mejor_recorrido[i]] for i in range(num_nodos))

    mejor_recorrido_nodos = [nodos[i] for i in mejor_recorrido]

    print("Mejor recorrido:", mejor_recorrido_nodos)
    print("Distancia total:", distancia_total)

if __name__ == "__main__":
    main()
