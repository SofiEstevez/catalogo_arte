# ¿Qué es este progama?

Un sencillo programa en Python para gestionar un catalogo de obras de arte. 
Permite consultar información de las obras, agregar nuevas y guardar información sobre si el usuario las visito o no.
Este programa incluyo un historial de errores.
---

## Funcionalidades

- Agregar nuevas obras al catalogo
- Consultar obras por ID de catalogo, titulo, artista o año.
- Marcar obras como visitadas

---

## Requisitos

- Python 3.7 o superior
- Pip (para instalar dependencias)

---

## Instalacion y configuracion del entorno

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/tu-usuario/tu-repo.git
   cd tu-repo


2. Crear/activar el entorno virtual (ejemplo usando venv)
    a. En Windows
```bash
    python -m venv env
    .\env\Scripts\activate

    b. En Mac / linux 
```bash
    python3 -m venv env
    source env/bin/activate

3. Instalar las dependencias especificadas en requirements.txt
```bash
pip install -r requirements.txt

4. Ejecutar el programa
python main.py

5. Al terminar de trabajar, desactivar entorno
activate


# Esctructura del proyecto
final/
├── catalogo.py             # Funciones con la logica detras de las opciones del menu principal
├── main.py                 # Menú principal, opciones que llama el usuario
├── catalogo.csv            # Archivo donde se guarda toda la informacion de las obras
├── history.log             # Logs del sistema. Aqui se guarda un historial de errores
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Este archivo
