from catalogo import agregar_obra, marcar_visitada, consultar_obra
#crear_tarea, guardar_tarea_en_csv, marcar_visitada, mostrar_tareas, eliminar_tarea

def menu():
    print("Menu")
    print("1. Agregar una obra al catalogo")
    print("2. Marcar obra como visitada")
    print("3. Consultar obra")
    eleccion = input("Seleccione una opcion: ")
    return eleccion
def main():
    while True:
        opcion = menu()
        if opcion == "1":
            agregar_obra()
        elif opcion == "2":
            marcar_visitada()
        elif opcion == "3":
            consultar_obra()

if __name__ == "__main__":
    main()