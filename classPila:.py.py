class Pila:
    def __init__(self):
        self.items = []

    def apilar(self, item):
        self.items.append(item)

    def desapilar(self):
        return self.items.pop()


def evaluar_prefija(expresion):
    pila = Pila()
    tokens = expresion.strip().split()
    
    # Recorrido de derecha a izquierda
    tokens.reverse()

    operadores = {'+', '-', '*', '/'}

    for token in tokens:
        if token in operadores:
            op1 = pila.desapilar()
            op2 = pila.desapilar()
            
            if token == '+': res = op1 + op2
            elif token == '-': res = op1 - op2
            elif token == '*': res = op1 * op2
            elif token == '/': res = op1 / op2
            
            pila.apilar(res)
        else:
            pila.apilar(float(token))

    return pila.desapilar()


# Bucle interactivo
while True:
    entrada = input("\nIngresa una expresión prefija (o 'salir' para terminar): ")
    
    if entrada.lower() == 'salir':
        print("Programa finalizado.")
        break
        
    try:
        resultado = evaluar_prefija(entrada)
        print(f"-> Resultado: {resultado}")
    except Exception as e:
        print("Error al evaluar. Asegúrate de separar con espacios números y operadores.")