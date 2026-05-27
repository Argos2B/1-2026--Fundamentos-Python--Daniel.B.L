# =========================================
# ACTIVIDAD 4 - REGISTRO DE ESTUDIANTES
# =========================================

archivo = "estudiantes.txt"

while True:
    print("\n===== MENÚ =====")
    print("1. Registrar estudiante")
    print("2. Mostrar cantidad de estudiantes")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        nombre = input("Ingrese el nombre del estudiante: ")
        carne = input("Ingrese el carné: ")
        nota = input("Ingrese la nota final: ")

        with open(archivo, "a") as f:
            f.write(f"Nombre: {nombre}, Carné: {carne}, Nota: {nota}\n")

        print("✅ Estudiante registrado correctamente.")

    elif opcion == "2":
        try:
            with open(archivo, "r") as f:
                estudiantes = f.readlines()
                print(f"📚 Cantidad de estudiantes registrados: {len(estudiantes)}")
        except FileNotFoundError:
            print("⚠️ No hay estudiantes registrados todavía.")

    elif opcion == "3":
        print("👋 Saliendo del programa...")
        break

    else:
        print("❌ Opción inválida.")