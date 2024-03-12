import os
import fitz  # PyMuPDF
import win32print
import win32api
from PIL import Image
import subprocess

# Diccionario para rastrear las páginas impresas
paginas_impresas = {}

def imprimir_hojas_pdf(archivo_pdf, impresora_predeterminada):
    doc = fitz.open(archivo_pdf)

    # Imprimir todas las páginas en orden inverso (desde la última hasta la primera)
    for pagina_num in range(doc.page_count - 1, -1, -1):
        pagina = doc[pagina_num]
        imagen = pagina.get_pixmap()

        # Convertir la imagen a formato BMP para impresión
        bmp_nombre_archivo = f"imgs\pagina_{pagina_num + 1}.bmp"
        imagen_pil = Image.frombytes("RGB", [imagen.width, imagen.height], imagen.samples)
        imagen_pil.save(bmp_nombre_archivo)

        # Verificar si la página ya ha sido impresa
        if not paginas_impresas.get(archivo_pdf, {}).get(pagina_num, False):
            subprocess.run(["mspaint.exe", "/pt", bmp_nombre_archivo, impresora_predeterminada])
            # Marcar la página como impresa
            paginas_impresas.setdefault(archivo_pdf, {})[pagina_num] = True

    doc.close()

def procesar_carpeta(carpeta, impresora_predeterminada):
    for archivo in os.listdir(carpeta):
        ruta_completa = os.path.join(carpeta, archivo)
        if os.path.isfile(ruta_completa) and archivo.lower().endswith('.pdf'):
            imprimir_hojas_pdf(ruta_completa, impresora_predeterminada)

def imprimir_pdf_en_carpeta(directorio, impresora_predeterminada):
    for root, dirs, files in os.walk(directorio):
        for directorio_actual in dirs:
            procesar_carpeta(os.path.join(root, directorio_actual), impresora_predeterminada)
        for archivo in files:
            ruta_completa = os.path.join(root, archivo)
            if archivo.lower().endswith('.pdf'):
                imprimir_hojas_pdf(ruta_completa, impresora_predeterminada)

if __name__ == "__main__":
    directorio_base = "C:/Users/llore/BackEnd/imp/Papers"
    impresora_predeterminada = win32print.GetDefaultPrinter()
    imprimir_pdf_en_carpeta(directorio_base, impresora_predeterminada)
