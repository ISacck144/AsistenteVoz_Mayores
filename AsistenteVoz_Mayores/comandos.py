import os
import subprocess

def abrir_chrome(hablar, url=None):
    # Ruta típica de instalación de Chrome en Windows
    rutas_posibles = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    chrome_path = None
    for ruta in rutas_posibles:
        if os.path.exists(ruta):
            chrome_path = ruta
            break

    if chrome_path:
        if url:
            subprocess.Popen([chrome_path, url])
            hablar(f"Abriendo Google Chrome en {url}")
        else:
            subprocess.Popen([chrome_path])
            hablar("Abriendo Google Chrome.")
    else:
        hablar("No encontré Google Chrome instalado en esta computadora.")