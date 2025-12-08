# text to speech using pyttsx3
import pyttsx3
import os

def texto_a_voz(input_txt_path: str, output_audio_path: str) -> None:
    """
    Lee un archivo de texto, genera un audio con pyttsx3 y lo guarda (sobrescribe si existe).
    Args:
      input_txt_path: ruta al .txt con el contenido a hablar
      output_audio_path: ruta del archivo de audio a generar (.wav o .mp3)
    """
    try:
        # Leer texto
        with open(input_txt_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Inicializar pyttsx3
        engine = pyttsx3.init()

        # Configuración de voz
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # Usa la voz femenina, cambia el índice para la masculina

        # Guardar el audio en el archivo especificado
        engine.save_to_file(text, output_audio_path)
        engine.runAndWait()

        print(f"Audio generado en: {output_audio_path}")
    
    except Exception as e:
        print(f"Error al generar el audio: {e}")

if __name__ == "__main__":
    # prueba
    print("Esto es una prueba de TTS con pyttsx3.")
    print("Generando audio desde texto...")
    txt_path = "prueba.txt"
    audio_path = "pruebalow.wav"
    texto_a_voz(txt_path, audio_path)