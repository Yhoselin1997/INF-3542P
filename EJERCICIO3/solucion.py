import random
import numpy

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

def generate_individual():
    return random.sample(range(NB_AGENTE), NB_AGENTE)

def crossover(parent1, parent2):
    point1 = random.randint(0, NB_AGENTE - 1)
    point2 = random.randint(0, NB_AGENTE - 1)
    start, end = min(point1, point2), max(point1, point2)
    child = parent1[start:end] + [gene for gene in parent2 if gene not in parent1[start:end]]
    return child

def mutate(individual):
    idx1, idx2 = random.sample(range(NB_AGENTE), 2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]

def select_population(population, fitnesses, k):
    selected_indices = sorted(range(len(fitnesses)), key=lambda i: fitnesses[i])[:k]
    return [population[i] for i in selected_indices]

def eaSimple(population, cxpb, mutpb, ngen):
    for gen in range(ngen):
        offspring = []
        for _ in range(len(population)):
            if random.random() < cxpb:  
                parent1, parent2 = random.sample(population, 2)
                child = crossover(parent1, parent2)
            else:  
                child = random.choice(population)

            if random.random() < mutpb:  
                mutate(child)

            offspring.append(child)

        offspring_fitness = [evalAgente(ind) for ind in offspring]

        population_and_fitness = list(zip(population + offspring, fitnesses + offspring_fitness))
        population, fitnesses = zip(*select_population(*zip(*population_and_fitness), len(population)))

    return population, fitnesses

def main(seed=0):
    random.seed(seed)

    population = [generate_individual() for _ in range(300)]
    fitnesses = [evalAgente(ind) for ind in population]

    hof = min(zip(population, fitnesses), key=lambda x: x[1])
    best_route_indices = hof[0]
    best_route_nodes = [chr(ord('A') + idx) for idx in best_route_indices]

    print("Mejor recorrido encontrado:", best_route_nodes)
    print("Distancia mínima:", hof[1][0])

if __name__ == "__main__":
    main()
