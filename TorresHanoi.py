def hanoi(n, origen, destino, auxiliar, a="A", c="C", b="B"):
    if n > 0:
        # 1. Mover n-1 discos de origen a auxiliar
        hanoi(n - 1, origen, auxiliar, destino, a, b, c)
        
        # 2. Mover disco actual
        disco = origen.pop()
        destino.append(disco)
        print(f"Mover disco {disco} de Torre {a} -> Torre {c}")
        
        # 3. Mover n-1 discos de auxiliar a destino
        hanoi(n - 1, auxiliar, destino, origen, b, c, a)

# Prueba para 3 discos:
A, B, C = [3, 2, 1], [], []
hanoi(len(A), A, C, B)