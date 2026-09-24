# ==========================================
# PROGRAMA DE VENTAS
# ==========================================

meses = [
    "Enero", "Febrero", "Marzo", "Abril",
    "Mayo", "Junio", "Julio", "Agosto",
    "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

departamentos = [
    "Ropa",
    "Deportes",
    "Juguetería"
]

# Crear la tabla vacía
# Cada departamento tendrá 12 espacios, uno por cada mes
ventas = []

for departamento in departamentos:
    fila = []
    for mes in meses:
        fila.append(0)
    ventas.append(fila)


# ==========================================
# MOSTRAR TABLA
# ==========================================

def mostrar_tabla():
    print("\n" + "=" * 115)
    print("                         TABLA DE VENTAS")
    print("=" * 115)

    print(f"{'Departamento':<18}", end="")

    for mes in meses:
        print(f"{mes:<8}", end="")

    print()
    print("-" * 115)

    for i in range(len(departamentos)):
        print(f"{departamentos[i]:<18}", end="")

        for j in range(len(meses)):
            print(f"${ventas[i][j]:<7.2f}", end="")

        print()

    print("=" * 115)


# ==========================================
# INSERTAR O ACTUALIZAR VENTA
# ==========================================

def insertar_actualizar():
    print("\n===== INSERTAR O ACTUALIZAR VENTA =====")

    print("\nDepartamentos:")
    for i in range(len(departamentos)):
        print(f"{i + 1}. {departamentos[i]}")

    try:
        opcion_departamento = int(input("\nSeleccione el departamento: "))

        if opcion_departamento < 1 or opcion_departamento > len(departamentos):
            print("Departamento no válido.")
            return

        departamento = opcion_departamento - 1

        print("\nMeses:")
        for i in range(len(meses)):
            print(f"{i + 1}. {meses[i]}")

        opcion_mes = int(input("\nSeleccione el mes: "))

        if opcion_mes < 1 or opcion_mes > len(meses):
            print("Mes no válido.")
            return

        mes = opcion_mes - 1

        monto = float(input("\nIngrese el monto de la venta: $"))

        if monto < 0:
            print("El monto no puede ser negativo.")
            return

        ventas[departamento][mes] = monto

        print("\nVenta registrada correctamente.")
        print(
            f"{departamentos[departamento]} - "
            f"{meses[mes]}: ${monto:.2f}"
        )

    except ValueError:
        print("\nDebe ingresar un número válido.")


# ==========================================
# BUSCAR VENTA POR MONTO
# ==========================================

def buscar_por_monto():
    print("\n===== BUSCAR VENTA POR MONTO =====")

    try:
        monto_buscar = float(
            input("Ingrese el monto que desea buscar: $")
        )

        encontrados = False

        for i in range(len(departamentos)):
            for j in range(len(meses)):

                if ventas[i][j] == monto_buscar:
                    print(
                        f"\nVenta encontrada:"
                        f"\nDepartamento: {departamentos[i]}"
                        f"\nMes: {meses[j]}"
                        f"\nMonto: ${ventas[i][j]:.2f}"
                    )

                    encontrados = True

        if not encontrados:
            print("\nNo se encontró ninguna venta con ese monto.")

    except ValueError:
        print("\nDebe ingresar un monto válido.")


# ==========================================
# ELIMINAR VENTA
# ==========================================

def eliminar_venta():
    print("\n===== ELIMINAR VENTA =====")

    print("\nDepartamentos:")
    for i in range(len(departamentos)):
        print(f"{i + 1}. {departamentos[i]}")

    try:
        opcion_departamento = int(
            input("\nSeleccione el departamento: ")
        )

        if opcion_departamento < 1 or opcion_departamento > len(departamentos):
            print("Departamento no válido.")
            return

        departamento = opcion_departamento - 1

        print("\nMeses:")
        for i in range(len(meses)):
            print(f"{i + 1}. {meses[i]}")

        opcion_mes = int(
            input("\nSeleccione el mes: ")
        )

        if opcion_mes < 1 or opcion_mes > len(meses):
            print("Mes no válido.")
            return

        mes = opcion_mes - 1

        if ventas[departamento][mes] == 0:
            print("\nNo existe una venta registrada en esa posición.")
            return

        print(
            f"\nVenta actual: ${ventas[departamento][mes]:.2f}"
        )

        confirmar = input(
            "¿Está seguro de eliminarla? (S/N): "
        ).upper()

        if confirmar == "S":
            ventas[departamento][mes] = 0
            print("\nVenta eliminada correctamente.")
        else:
            print("\nOperación cancelada.")

    except ValueError:
        print("\nDebe ingresar un número válido.")


# ==========================================
# BUSCAR UNA VENTA ESPECÍFICA
# ==========================================

def buscar_venta_especifica():
    print("\n===== BUSCAR UNA VENTA ESPECÍFICA =====")

    print("1. Buscar por departamento y mes")
    print("2. Buscar por monto")
    print("3. Regresar")

    try:
        opcion = int(input("\nOpción: "))

        if opcion == 1:

            print("\nDepartamentos:")
            for i in range(len(departamentos)):
                print(f"{i + 1}. {departamentos[i]}")

            dep = int(input("\nSeleccione el departamento: "))

            if dep < 1 or dep > len(departamentos):
                print("Departamento no válido.")
                return

            print("\nMeses:")
            for i in range(len(meses)):
                print(f"{i + 1}. {meses[i]}")

            mes = int(input("\nSeleccione el mes: "))

            if mes < 1 or mes > len(meses):
                print("Mes no válido.")
                return

            departamento = dep - 1
            mes_real = mes - 1

            monto = ventas[departamento][mes_real]

            print("\n===== VENTA ENCONTRADA =====")
            print(f"Departamento: {departamentos[departamento]}")
            print(f"Mes: {meses[mes_real]}")
            print(f"Monto: ${monto:.2f}")

        elif opcion == 2:
            buscar_por_monto()

        elif opcion == 3:
            return

        else:
            print("\nOpción no válida.")

    except ValueError:
        print("\nDebe ingresar un número válido.")


# ==========================================
# MENÚ PRINCIPAL
# ==========================================

while True:

    print("\n")
    print("=" * 40)
    print("          MENÚ DE VENTAS")
    print("=" * 40)
    print("1. Insertar o actualizar ventas")
    print("2. Buscar venta por monto")
    print("3. Eliminar venta")
    print("4. Visualizar tabla de ventas")
    print("5. Buscar una venta específica")
    print("6. Salir")
    print("=" * 40)

    try:
        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:
            insertar_actualizar()

        elif opcion == 2:
            buscar_por_monto()

        elif opcion == 3:
            eliminar_venta()

        elif opcion == 4:
            mostrar_tabla()

        elif opcion == 5:
            buscar_venta_especifica()

        elif opcion == 6:
            print("\nPrograma finalizado.")
            break

        else:
            print("\nOpción no válida.")

    except ValueError:
        print("\nDebe ingresar un número del menú.")
