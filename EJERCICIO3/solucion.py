import random
import numpy as np

random.seed(42)

grafo = np.loadtxt("agente1.csv",delimiter=";")

num_nodos = len(grafo)

nodos = ["A", "B", "C", "D", "E"]

def evaluar_recorrido(individuo):
    distancia_total = sum(grafo[individuo[i - 1]][individuo[i]] for i in range(num_nodos))
    return distancia_total,

def cruzar(padre1, padre2):
    punto_cruza = random.randint(0, num_nodos - 1)
    hijo = [-1] * num_nodos

    hijo[:punto_cruza] = padre1[:punto_cruza]

    j = punto_cruza
    for gen in padre2:
        if gen not in hijo:
            hijo[j] = gen
            j = (j + 1) % num_nodos

    return hijo

def mutar(individuo):
    i, j = random.sample(range(num_nodos), 2)
    individuo[i], individuo[j] = individuo[j], individuo[i]

pop_size = 100
num_generaciones = 500
prob_cruce = 0.7
prob_mutacion = 0.2

poblacion = [random.sample(range(num_nodos), num_nodos) for _ in range(pop_size)]

for generacion in range(num_generaciones):
    aptitudes = [evaluar_recorrido(individuo) for individuo in poblacion]

    padres_seleccionados = [poblacion[i] for i in random.sample(range(pop_size), pop_size)]

    descendencia = []
    for i in range(0, pop_size, 2):
        padre1, padre2 = padres_seleccionados[i], padres_seleccionados[i + 1]

        if random.random() < prob_cruce:
            hijo1 = cruzar(padre1, padre2)
            hijo2 = cruzar(padre2, padre1)
        else:
            hijo1, hijo2 = padre1[:], padre2[:]

        if random.random() < prob_mutacion:
            mutar(hijo1)
        if random.random() < prob_mutacion:
            mutar(hijo2)

        descendencia.extend([hijo1, hijo2])

    poblacion = descendencia

aptitudes = [evaluar_recorrido(individuo) for individuo in poblacion]

mejor_individuo = min(poblacion, key=lambda ind: evaluar_recorrido(ind)[0])

mejor_recorrido_nodos = [nodos[i] for i in mejor_individuo]
distancia_total = evaluar_recorrido(mejor_individuo)[0]

print("Mejor recorrido:", mejor_recorrido_nodos)
print("Distancia total:", distancia_total)
