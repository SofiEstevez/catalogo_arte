
import os
import logging
import csv
import unicodedata
from rich.console import Console
from rich.table import Table

console = Console()

archivo = 'catalogo.csv'

logging.basicConfig(
    filename='catalogo.log',        
    level=logging.INFO,            
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def normalizar_texto(texto):
    '''
    Esta funcion normaliza los inputs del usuario cuando se busca un titulo, para que el usuario pueda
    buscar el titulo de una obra con mayusculas, minusculas, con y sin tiildes.
    Para eso, convierte texto a minusculas y elimina tildes.
    '''
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    return ''.join(c for c in texto if unicodedata.category(c) != 'Mn')

def agregar_obra():
    '''
    Esta funcion agrega una obra al catalogo.
    Pregunta el titulo al usuario y verifica si la obra ya existe.
    Si existe, no permite agregarla de nuevo.
    Si no existe, le pregunta al usuario el resto de los datos y crea una nueva obra
    '''
    try:
        encabezado = ["id", "titulo", "año", "autor", "estilo", "museo", "ciudad", "pais", "visitada", "opinion"]

        # Verifico si existe el archivo y lo abro para leer
        if not os.path.exists(archivo) or os.stat(archivo).st_size == 0:
            # Si no existe, creo el archivo y el encabezado 
            with open(archivo, "wt", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(encabezado)
            logging.info("Archivo creado con encabezado.")

        else:
            # Si existe, verifico que tenga el encabezado correcto
            with open(archivo, "rt", encoding="utf-8") as f:
                reader = csv.reader(f)
                actual = next(reader)
            if actual != encabezado:
                # Reescribo el encabezado correcto + datos existentes
                with open(archivo, "rt", encoding="utf-8") as f:
                    datos = list(csv.reader(f))[1:]  # excluyo encabezado viejo
                with open(archivo, "wt", newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(encabezado)
                    writer.writerows(datos)
                logging.info("Encabezado corregido en archivo existente.")


        # Leer datos existentes
        with open(archivo, "rt", encoding="utf-8") as f:
            reader = list(csv.reader(f))
            filas = reader[1:]  # datos sin encabezado

        # Pido título y busco si existe
        titulo_nuevo = input("Ingrese el título de la obra: ").strip()
        obra_existente = None
        for fila in filas:
            if len(fila) > encabezado.index("titulo") and normalizar_texto(fila[encabezado.index("titulo")].strip()) == normalizar_texto(titulo_nuevo):
            #fila[encabezado.index("titulo")].strip().lower() == titulo_nuevo.lower():
                obra_existente = fila
                break

        if obra_existente:
            print("La obra ya existe en el catálogo:")
            print(obra_existente)
            logging.warning(f"Intento de agregar obra existente: título='{titulo_nuevo}'")
            return
        
        # Si no existe, pido los demás datos
        # pido el año y compruebo que sea un numero
        while True:
            año = input("Ingrese el año de la obra: ").strip()
            if año.isdigit():
                break # sigo a preguntar los demas datos
            else:
                print("Por favor ingrese un número válido para el año.")

        autor = input("Ingrese el autor de la obra: ").strip()
        estilo = input("Ingrese el estilo de la obra: ").strip()
        museo = input("Ingrese el museo donde se encuentra la obra: ").strip()
        ciudad = input("Ingrese la ciudad del museo: ").strip()
        pais = input("Ingrese el país del museo: ").strip()

        # pido el dato de si visito o no la obra. Recibo la respuesta en numero y la transformo en false o true
        while True:
            visitado_rsta = input("¿Ya visitaste esta obra? (Ingresa 1: para responder Sí, o 2 para responder No): ").strip()
            if visitado_rsta == "1":
                visitado = "True"
                break # respuesta valida, sigo a preguntar opinion
            elif visitado_rsta == "2":
                visitado = "False"
                break # respuesta valida, sigo a preguntar opinion
            else:
                print("El valor ingresado es invalido.")

        #ultima pregunta al usuario, le pido la opinion.        
        opinion = input("Escribe tu opinión sobre la obra: ").strip()

        # Genero un nuevo ID: busco el max ID y le sumo 1 o le doy ID 1 si el archivo está vacío
        ids = [int(fila[encabezado.index("id")]) for fila in filas if fila[encabezado.index("id")].isdigit()]
        nuevo_id = str(max(ids) + 1) if ids else "1"

        nueva_obra = [
            nuevo_id,
            titulo_nuevo,
            año,
            autor,
            estilo,
            museo,
            ciudad,
            pais,
            visitado,
            opinion
        ]

        # Agrego la nueva obra al CSV
        with open(archivo, "at", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(nueva_obra)

        print("Obra agregada correctamente al catálogo.")
        print(nueva_obra)
        logging.info(f"Obra agregada: ID={nuevo_id}, título='{titulo_nuevo}'")


    except Exception as e:
        logging.error(f"Error en agregar_obra: {e}")
        print("Ocurrió un error:", e)



def marcar_visitada():
    '''
    Esta funcion marca una obra como visitada.
    Le pide al usuario un ID o titulo para buscar la obra
    Luego verifica que esa obra exista y aun no haya sido marcada como visitada. Si es asi, la marca como visitada.
    Si la obra no existe, da error
    Si la obra existe pero ya esta marcada como visitada, da error.
    '''

    # Leer todas las líneas
    with open(archivo, "rt", encoding="utf-8") as f:
        lineas = f.readlines()

    # Guardo la primera línea como el encabezado
    encabezado = lineas[0].strip().split(",")
    
    # Busco la columna 'visitada' y me guardo su index
    try:
        index_visitada = encabezado.index("visitada")
    except ValueError:
        print("La columna 'visitada' no existe en el CSV.")
        return

    print("¿Cómo querés buscar la obra?")
    print("1. Por ID")
    print("2. Por título")

    opcion = input("Elegí una opción (1 o 2): ").strip()


    encontrada = False
    nuevas_lineas = [lineas[0]]

    # si usuario quiere buscar por id
    if opcion == "1":
        valor = input("Ingresá el ID a buscar: ").strip()
        # me guardo el index del campo id
        index_id = encabezado.index("id")
        cambio_realizado = False

        # recorro todas las lineas (excepto el encabezado), divido cada obra en una lista de valores, usando la coma como separador
        for linea in lineas[1:]:
            partes = linea.strip().split(",")
        # en cada vuelta, comparo el id de esa linea con el valor ingresado por el usuario
            if partes[index_id].strip() == valor:
                encontrada = True
                if partes[index_visitada] == "True":
                    print("La obra ya fue marcada como visitada")

                else:
                    partes[index_visitada] = "True"
                    print(f"Obra encontrada: {partes}")
                    cambio_realizado = True
                    logging.info(f"La obra con id {partes[index_id]} fue marcada como visitada.")
            # reconstruyo siempre la línea (modificada o no)
            nuevas_lineas.append(",".join(partes) + "\n")
        # si encontre la obra, rescribo el CSV para guardar los cambios.
        if encontrada:
            if cambio_realizado:
                with open(archivo, "wt", encoding="utf-8") as stream:
                    stream.writelines(nuevas_lineas)
                print("Cambios guardados")
            else:
                print("No se realizaron cambios.")
        else:
            print("No existe una obra con ese ID")

    # si usuario quiere buscar por titulo
    elif opcion == "2":
        valor = input("Ingresá el título de la obra: ").strip()
        valor_normalizado = normalizar_texto(valor)
        # guardo el index del campo titulo
        index_titulo = encabezado.index("titulo")
        # recorro todas lineas excepto el encabezado. por cada vuelta, creo una lista con los valores de una obra
        for linea in lineas[1:]:
            partes = linea.strip().split(",")
            titulo_normalizado = normalizar_texto(partes[index_titulo].strip())
            # si encuentro el titulo
            if titulo_normalizado == valor_normalizado:
                encontrada = True
                if partes[index_visitada] == "True":
                    print("La obra ya fue marcada como visitada")
                else:
                    partes[index_visitada] = "True"
                    print(f"Obra encontrada y marcada como visitada: {partes}")
                    logging.info(f"La obra {partes} fue marcada como visitada.")
                encontrada = True
            # reconstruyo el CSV, tanto si encontre la obra o no, si la cambie o no
            nuevas_lineas.append(",".join(partes) + "\n")
        # si encontre una obra con ese titulo, guardo
        if encontrada:
            with open(archivo, "wt", encoding="utf-8") as stream:
                stream.writelines(nuevas_lineas)
            print("Cambios guardados")
        else:
            print("No se encontró ninguna obra con ese título.")

    # si no eligio buscar por id o titulo
    else:
        print("El valor ingresado es invalido")
        return

def consultar_obra():
    '''
    Esta funcion permite a un usuario consultar informacion sobre una obra.
    Permite buscar obras por ID, título, artista o año.
    Si la obra no se encuentra en el catalogo, da error
    '''
    try:
        with open(archivo, "rt", encoding="utf-8") as f:
            lineas = f.readlines()

        encabezado = lineas[0].strip().split(",")

        print("¿Cómo querés buscar la obra?")
        print("1. Por ID")
        print("2. Por título")
        print("3. Por artista")
        print("4. Por año")

        opcion = input("Elegí una opción (1, 2, 3 o 4): ").strip()
        encontradas = []

        if opcion == "1":
            valor = input("Ingresá el ID a buscar: ").strip()
            index_id = encabezado.index("id")
            for linea in lineas[1:]:
                    partes = linea.strip().split(",")
                    if partes[index_id].strip() == valor:
                        encontradas.append(partes)
                        break  # ID es único

            if encontradas:
                tabla = Table(title=f"Obra con ID '{valor}'")
                for columna in encabezado:
                    tabla.add_column(columna.capitalize(), style="cyan", no_wrap=True)

                tabla.add_row(*encontradas[0])
                console.print(tabla)
            else:
                print("No existe una obra con ese ID.")


# buscar obra por titulo
        elif opcion == "2":
            valor = input("Ingresá el título de la obra: ").strip()
            valor_normalizado = normalizar_texto(valor)
            index_titulo = encabezado.index("titulo")

            for linea in lineas[1:]:
                partes = linea.strip().split(",")
                titulo_normalizado = normalizar_texto(partes[index_titulo].strip())
                if titulo_normalizado == valor_normalizado:
                    encontradas.append(partes)
                    break

            if encontradas:
                tabla = Table(title=f"Obra con título '{valor}'")
                for columna in encabezado:
                    tabla.add_column(columna.capitalize(), style="cyan", no_wrap=True)

                tabla.add_row(*encontradas[0])
                console.print(tabla)
            else:
                print("No se encontró ninguna obra con ese título.")

# busqueda por nombre del artista
        elif opcion == "3":
            valor = input("Ingresá el nombre del artista: ").strip().lower()
            index_artista = encabezado.index("artista")

            for linea in lineas[1:]:
                partes = linea.strip().split(",")
                if partes[index_artista].strip().lower() == valor:
                    encontradas.append(partes)

            if encontradas:
                tabla = Table(title=f"Obras del artista '{valor}'")
                for columna in encabezado:
                    tabla.add_column(columna.capitalize(), style="cyan", no_wrap=True)
                for partes in encontradas:
                    tabla.add_row(*partes)
                console.print(tabla)
            else:
                print("No se encontraron obras de ese artista.")     


# busqueda por año
        elif opcion == "4":
            valor = input("Ingresá el año de la obra: ").strip()
            index_anio = encabezado.index("año")

            for linea in lineas[1:]:
                partes = linea.strip().split(",")
                if partes[index_anio].strip() == valor:
                    encontradas.append(partes)

            if encontradas:
                tabla = Table(title=f"Obras del año '{valor}'")
                for columna in encabezado:
                    tabla.add_column(columna.capitalize(), style="cyan", no_wrap=True)

                for partes in encontradas:
                    tabla.add_row(*partes)
                console.print(tabla)
            else:
                print("No se encontraron obras de ese año.")

        else:
            print("El valor ingresado es inválido.")

    except FileNotFoundError:
        print("El archivo del catálogo no existe todavía.")
    except Exception as e:
        print("Ocurrió un error:", e)




###################################################################

# falta
    # documentar las funciones
    # en busqueda por titulo, agregar tratamiento de mayus y de tildes
