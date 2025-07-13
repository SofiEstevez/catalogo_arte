# ¿Qué es este progama?

Un sencillo programa escrito en Python para gestionar un catálogo de obras de arte.
Permite consultar la informacoin de las obras, agregar nuevas y guardar información sobre si el usuario las visitó o no, así como cambiar a "visitado" una vez que hayas visitado una obra.


## Funcionalidades

- Agregar nuevas obras al catalogo
- Consultar obras por ID de catalogo, titulo, artista o año.
- Marcar obras como visitadas


## Requisitos

- Python 3.7 o superior
- Pip (para instalar dependencias)



## Instalacion y configuracion del entorno

1. Clonar el repositorio  
```bash
   git clone https://github.com/SofiEstevez/catalogo_arte.git
```

2. Crear/activar el entorno virtual (ejemplo usando venv)
 2a En Windows
   
```bash
    python -m venv env
    .\env\Scripts\activate
```

b. En Mac / Linux
    
```bash
    python3 -m venv env
    source env/bin/activate
```


3. Instalar las dependencias especificadas en requirements.txt

```bash
pip install -r requirements.txt
```

4. Ejecutar el programa

```bash
python main.py
```

5. Al terminar de trabajar, desactivar entorno
```bash
deactivate
```


# Estructura del proyecto

```plaintext
final/
├── catalogo.py             # Funciones con la lógica detrás de las opciones del menú principal
├── main.py                 # Menú principal, opciones que llama el usuario
├── catalogo.csv            # Archivo donde se guarda toda la información de las obras
├── history.log             # Logs del sistema. Aquí se guarda un historial de errores
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Este archivo

