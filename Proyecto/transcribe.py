from escuchaclave import escuchar_y_transcribir
import whisper
import time
import pyaudio
import numpy as np

# =========================
# CONFIGURACIÓN GENERAL
# =========================
formato = pyaudio.paInt16
canales = 1
tasa_muestreo = 16000
frames_por_buffer = 1024

def grabar_y_transcribir_audio(duracion=10):
    """Graba y transcribe el audio después de la palabra clave detectada."""
    
    print("[INFO] Iniciando la grabación...")

    p = pyaudio.PyAudio()
    stream = p.open(
        format=formato,
        channels=canales,
        rate=tasa_muestreo,
        input=True,
        frames_per_buffer=frames_por_buffer
    )
    
    frames = []
    print("[INFO] Grabando...")
    
    # Grabación durante 'duracion' segundos
    for _ in range(int(tasa_muestreo / frames_por_buffer * duracion)):
        data = stream.read(frames_por_buffer)
        frames.append(data)
    
    print("[INFO] Grabación finalizada.")

    # Convertir audio (PCM16) a float32 para Whisper
    raw = b"".join(frames)
    audio_np = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

    # Cargar el modelo de Whisper y transcribir el audio grabado
    model = whisper.load_model("base")
    result = model.transcribe(audio_np, language="es")
    texto_transcrito = result.get("text", "").strip()

    stream.stop_stream()
    stream.close()

    return texto_transcrito


def ejecutar_transcripcion():
    print("[INFO] Iniciando el proceso de escucha y transcripción...")
    
    resultado = escuchar_y_transcribir()  # Llamada al módulo que detecta la palabra clave
    if resultado:
        print("[INFO] Palabra clave detectada. Ahora transcribiendo lo que sigue...")

        # Esperar 2 segundos después de la palabra clave
        print("[INFO] Esperando 2 segundos de silencio...")
        time.sleep(2)

        # Después de la palabra clave, grabar lo que diga el usuario
        texto_usuario = grabar_y_transcribir_audio(duracion=10)  # Puedes ajustar la duración según lo necesario

        if texto_usuario:
            print("[INFO] Transcripción finalizada, guardando en 'transcripcion.txt'...")

            # Guardar o sobrescribir la transcripción en el archivo
            with open("transcripcion.txt", "w") as file:
                file.write(texto_usuario)

            print("[INFO] Transcripción guardada en 'transcripcion.txt'")
        else:
            print("[INFO] No se captó ninguna entrada del usuario.")
    else:
        print("[INFO] No se detectó la palabra clave.")


if __name__ == "__main__":
    print("Ejecutando el módulo de transcripción, por favor ejecutar el main.py para la funcionalidad completa.")
    ejecutar_transcripcion()