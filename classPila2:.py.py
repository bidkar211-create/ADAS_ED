class Pila:
    def __init__(self):
        self.items = []

    def apilar(self, item):
        self.items.append(item)

    def desapilar(self):
        return self.items.pop()


def evaluar_posfija(expresion):
    pila = Pila()
    tokens = expresion.strip().split()

    operadores = {'+', '-', '*', '/'}

    for token in tokens:
        if token in operadores:
            op2 = pila.desapilar()
            op1 = pila.desapilar()
            
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
    entrada = input("\nIngresa una expresión posfija (o 'salir' para terminar): ")
    
    if entrada.lower() == 'salir':
        print("Programa finalizado.")
        break
        
    try:
        resultado = evaluar_posfija(entrada)
        print(f"-> Resultado: {resultado}")
    except Exception as e:
        print("Error al evaluar. Asegúrate de separar con espacios números y operadores.")