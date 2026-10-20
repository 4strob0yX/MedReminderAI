import heapq

grafo = {
    'A': [('B', 2), ('C', 5)],
    'B': [('D', 4), ('E', 1)],
    'C': [('F', 2), ('G', 8)],
    'D': [('H', 3)],
    'E': [('I', 2)],
    'F': [('J', 3)],
    'G': [],
    'H': [],
    'I': [],
    'J': []
}

inicio = 'A'
objetivo = 'J'

cola = [(0, inicio, [inicio])]
visitados = set()

while cola:
    costo, actual, ruta = heapq.heappop(cola)

    if actual == objetivo:
        print("Meta alcanzada!")
        print("Ruta final:", " -> ".join(ruta))
        print("Costo total:", costo)
        break

    if actual not in visitados:
        visitados.add(actual)
        for vecino, peso in grafo.get(actual, []):
            if vecino not in visitados:
                heapq.heappush(cola, (costo + peso, vecino, ruta + [vecino]))
