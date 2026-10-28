# Árbol del ejercicio
arbol = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H'],
    'E': [],
    'F': ['I', 'J'],
    'G': [],
    'H': [],
    'I': [],
    'J': []
}

# Heurísticas h(n)
h = {
    'A': 7, 'B': 6, 'C': 4, 'D': 7, 'E': 5,
    'F': 3, 'G': 6, 'H': 8, 'I': 1, 'J': 0
}

actual = 'A'
meta = 'J'
ruta = [actual]
total = 0

while actual != meta:
    hijos = arbol.get(actual, [])
    # Elegir el hijo con menor heurística (más prometedor)
    mejor_hijo = min(hijos, key=lambda nodo: h[nodo])
    
    total += h[mejor_hijo]
    actual = mejor_hijo
    ruta.append(actual)

print("Meta alcanzada!")
print("Ruta final:", " -> ".join(ruta))
print("Costo total:", total)
