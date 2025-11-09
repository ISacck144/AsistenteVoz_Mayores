import os
import time
import pyautogui
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
import google.generativeai as genai
import glob
from navegacion import (
    abrir_carpeta,
    navegar_a_subcarpeta,
    listar_contenido_actual,
    obtener_ruta_actual
)
from comandos import abrir_chrome

# Cargar variables del entorno (.env)
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Cambia aquí el modelo si lo necesitas
NOMBRE_DEL_MODELO = "models/gemini-2.5-flash"

# Configurar Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(NOMBRE_DEL_MODELO)

# Inicialización del motor de voz
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

def hablar(texto):
    print(f"Asistente: {texto}")
    engine.say(texto)
    engine.runAndWait()

def escuchar():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Escuchando... (habla ahora)")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        comando = r.recognize_google(audio, language='es-ES')
        print(f"Tú dijiste: {comando}")
        return comando.lower()
    except sr.UnknownValueError:
        hablar("No te entendí, ¿puedes repetirlo?")
        return ""
    except sr.RequestError:
        hablar("Parece que no hay conexión con el servicio de reconocimiento.")
        return ""

def interpretar_comando_ia(texto_usuario):
    """Usa Gemini para entender el contexto del comando del usuario."""
    prompt = f"""
    Eres un asistente virtual para adultos mayores. 
    Interpreta lo que el usuario quiere hacer en su computadora.
    Devuelve una acción clara en texto simple como:
    - "abrir navegador"
    - "abrir bloc de notas"
    - "enviar correo en gmail"
    - "salir"
    
    Usuario: "{texto_usuario}"
    """
    respuesta = model.generate_content(prompt)
    return respuesta.text.strip().lower()

def ejecutar_comando(comando):
    if "navegador" in comando or "chrome" in comando or "google" in comando:
        abrir_chrome(hablar)

    elif "bloc" in comando or "notas" in comando:
        hablar("Abriendo el bloc de notas.")
        pyautogui.press('win')
        time.sleep(1)
        pyautogui.typewrite("bloc de notas\n")

    elif "gmail" in comando or "correo" in comando:
        hablar("Abriendo Gmail en el navegador.")
        pyautogui.press('win')
        time.sleep(1)
        pyautogui.typewrite("chrome\n")
        time.sleep(2)
        pyautogui.typewrite("https://mail.google.com\n")

    elif "fotos" in comando or "imágenes" in comando or "imagenes" in comando:
        hablar("Abriendo la carpeta de imágenes.")
        ruta_imagenes = os.path.expanduser("~\\Pictures")
        os.startfile(ruta_imagenes)

    elif "documentos" in comando:
        hablar("Abriendo la carpeta de documentos.")
        ruta_documentos = os.path.expanduser("~\\Documents")
        os.startfile(ruta_documentos)

    elif "descargas" in comando:
        hablar("Abriendo la carpeta de descargas.")
        ruta_descargas = os.path.expanduser("~\\Downloads")
        os.startfile(ruta_descargas)

    elif "salir" in comando or "adiós" in comando:
        hablar("Adiós, que tengas un buen día.")
        exit()

    elif "mostrar fotos" in comando or "ver fotos" in comando:
        mostrar_todas_las_fotos()

    elif "listar fotos" in comando or "qué hay en fotos" in comando:
        ruta_imagenes = os.path.expanduser("~\\Pictures")
        listar_contenido_carpeta(ruta_imagenes)

    elif "abrir carpeta" in comando:
        nombre = comando.replace("abrir carpeta", "").strip()
        if nombre:
            posible_ruta = os.path.join(obtener_ruta_actual(), nombre)
            abrir_carpeta(posible_ruta, hablar)
        else:
            hablar("¿Qué carpeta quieres abrir?")
    elif "entrar a" in comando or "abrir" in comando:
        nombre = comando.replace("entrar a", "").replace("abrir", "").strip()
        if nombre:
            navegar_a_subcarpeta(nombre, hablar)
        else:
            hablar("¿A qué carpeta quieres entrar?")
    elif "dónde estoy" in comando or "ruta actual" in comando:
        hablar(f"Estás en la carpeta: {obtener_ruta_actual()}")
    elif "listar contenido" in comando or "qué hay aquí" in comando:
        listar_contenido_actual(hablar)

    else:
        hablar("No reconozco ese comando, pero seguiré aprendiendo.")

def mostrar_todas_las_fotos():
    ruta_imagenes = os.path.expanduser("~\\Pictures")
    # Busca archivos de imagen comunes
    patrones = ["*.jpg", "*.jpeg", "*.png", "*.bmp"]
    imagenes = []
    for patron in patrones:
        imagenes.extend(glob.glob(os.path.join(ruta_imagenes, patron)))
    if imagenes:
        for img in imagenes:
            os.startfile(img)
        hablar(f"He abierto {len(imagenes)} fotos.")
    else:
        hablar("No encontré fotos en tu carpeta de imágenes.")

def listar_contenido_carpeta(ruta):
    try:
        contenido = os.listdir(ruta)
        if contenido:
            hablar("Dentro de la carpeta tienes: " + ", ".join(contenido[:5]))
        else:
            hablar("La carpeta está vacía.")
    except Exception as e:
        hablar("No pude acceder a la carpeta.")

def main():
    hablar("Hola, soy tu asistente por voz. ¿En qué puedo ayudarte?")
    print("Modelos disponibles:")
    try:
        modelos = genai.list_models()
        for m in modelos:
            print(m.name)
    except Exception as e:
        print(f"Error al listar modelos: {e}")
        
    while True:
        texto_usuario = escuchar()
        if texto_usuario:
            comando = interpretar_comando_ia(texto_usuario)
            print(f"🤖 Interpretado por IA: {comando}")
            ejecutar_comando(comando)

if __name__ == "__main__":
    main()
