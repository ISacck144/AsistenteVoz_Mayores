import os

# Variable global para la ruta actual
ruta_actual = os.path.expanduser("~")  # Carpeta de usuario por defecto

def obtener_ruta_actual():
    global ruta_actual
    return ruta_actual

def abrir_carpeta(ruta, hablar):
    global ruta_actual
    if os.path.isdir(ruta):
        ruta_actual = ruta
        os.startfile(ruta)
        hablar(f"Abriendo la carpeta: {os.path.basename(ruta)}")
    else:
        hablar("No encontré esa carpeta.")

def navegar_a_subcarpeta(nombre_subcarpeta, hablar):
    global ruta_actual
    subcarpeta = os.path.join(ruta_actual, nombre_subcarpeta)
    if os.path.isdir(subcarpeta):
        abrir_carpeta(subcarpeta, hablar)
    else:
        hablar("No encontré esa subcarpeta.")

def listar_contenido_actual(hablar):
    global ruta_actual
    try:
        contenido = os.listdir(ruta_actual)
        if contenido:
            hablar("Dentro de la carpeta tienes: " + ", ".join(contenido[:5]))
        else:
            hablar("La carpeta está vacía.")
    except Exception:
        hablar("No pude acceder a la carpeta actual.")