import pyaudio
import whisper
import numpy as np
import os
import argparse
import subprocess  # Usamos subprocess para ejecutar el comando beep
import time  # Para la espera de unos segundos

# =========================
# CONFIGURACIÓN GENERAL
# =========================
def parse_args():
    parser = argparse.ArgumentParser(description="Sistema de escucha con palabra clave.")
    parser.add_argument('--palabra_clave', type=str, default="hola andador", help="Palabra clave a detectar")
    parser.add_argument('--duracion', type=int, default=5, help="Duración de escucha en segundos")
    return parser.parse_args()

args = parse_args()

formato = pyaudio.paInt16
canales = 1
tasa_muestreo = 16000
frames_por_buffer = 1024
palabra_clave = args.palabra_clave
duracion_escucha = args.duracion

print("[INFO] Cargando modelo Whisper en CPU...")
model = whisper.load_model("base")

p = pyaudio.PyAudio()

# =========================
# FUNCIONES AUXILIARES
# =========================

def listar_dispositivos_entrada(pya):
    """Lista micrófonos detectados"""
    print("\n[INFO] Dispositivos de audio disponibles:")
    found_input = False

    for i in range(pya.get_device_count()):
        info = pya.get_device_info_by_index(i)
        max_in = int(info.get("maxInputChannels", 0))
        nombre = info.get("name", "N/A")

        if max_in > 0:
            found_input = True
            print(f"  - ID {i}: {nombre} (canales entrada = {max_in})")

    if not found_input:
        print("[AVISO] No se encontraron micrófonos.")
    return found_input


def probar_con_archivo(archivo_audio, palabra_clave):
    """Modo prueba sin micrófono"""
    if not os.path.exists(archivo_audio):
        print(f"[ERROR] El archivo '{archivo_audio}' no existe.")
        return False

    print(f"\n[INFO] Modo prueba → Transcribiendo: {archivo_audio}")
    result = model.transcribe(archivo_audio, language="es")
    texto = result.get("text", "").strip()

    print("\n[TRANSCRIPCIÓN ARCHIVO]:")
    print(texto)

    if palabra_clave.lower() in texto.lower():
        print(f"\n[OK] Palabra clave '{palabra_clave}' detectada.")
        return True
    else:
        print(f"[INFO] No se detectó la palabra clave.")
        return False


def emitir_pitido():
    """Genera un pitido utilizando el comando beep"""
    subprocess.run(["beep", "-f", "1000", "-l", "500"])  # Frecuencia 1000 Hz, duración 500 ms


def escuchar_y_transcribir():
    print("[INFO] Iniciando modo escucha con micrófono...")

    hay_mic = listar_dispositivos_entrada(p)
    if not hay_mic:
        print("\n[AVISO] No hay micrófono. Modo prueba con archivo.\n")
        if probar_con_archivo("prueba.wav", palabra_clave):
            return True
        return False

    try:
        stream = p.open(
            format=formato,
            channels=canales,
            rate=tasa_muestreo,
            input=True,
            frames_per_buffer=frames_por_buffer
        )
        
        print("\n[INFO] Micrófono ABIERTO. Escuchando…")
        print("[INFO] Pronuncia la frase clave:", palabra_clave)

        while True:
            frames = []
            print("\n[DEBUG] Grabando", duracion_escucha, "segundos...")

            for _ in range(int(tasa_muestreo / frames_por_buffer * duracion_escucha)):
                data = stream.read(frames_por_buffer)
                frames.append(data)

            # Convertir audio (PCM16) a float32 para Whisper
            raw = b"".join(frames)
            audio_np = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

            print("[DEBUG] Transcribiendo fragmento…")
            result = model.transcribe(audio_np, language="es")
            texto = result.get("text", "").strip()

            print("[TRANSCRIPCIÓN]:", texto)

            if palabra_clave.lower() in texto.lower():
                print(f"\n[OK] ¡Palabra clave '{palabra_clave}' DETECTADA!")
                emitir_pitido()

                # Esperar un par de segundos para asegurar que el usuario no diga nada más
                time.sleep(2)

                # Ahora transcribir lo que diga el usuario después de la palabra clave
                print("\n[INFO] Comenzando transcripción...")

                frames.clear()
                for _ in range(int(tasa_muestreo / frames_por_buffer * 10)):  # Escuchar 10 segundos
                    data = stream.read(frames_por_buffer)
                    frames.append(data)

                raw = b"".join(frames)
                audio_np = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

                # Transcribir el nuevo audio
                result = model.transcribe(audio_np, language="es")
                texto_final = result.get("text", "").strip()
                print("[TRANSCRIPCIÓN FINAL]:", texto_final)

                # Guardar la transcripción en un archivo .txt
                with open("transcripcion.txt", "w") as file:
                    file.write(texto_final)

                return True  # Si la palabra clave fue detectada y la transcripción fue realizada correctamente

        return False  # Si la palabra clave no fue detectada, retornamos False

    except OSError as e:
        print(f"[ERROR] Problema con PyAudio: {e}")
        return True  # Aseguramos que el programa retorne True si la palabra clave fue detectada

    finally:
        print("[INFO] Cerrando stream de audio…")
        if 'stream' in locals():
            stream.stop_stream()
            stream.close()
    return False


# =========================
# EJECUCIÓN PRINCIPAL
# =========================

if __name__ == "__main__":
    print("Esta es la prueba del sistema de escucha con palabra clave, por favor corra el main.py.")
    resultado = escuchar_y_transcribir()
    print("[INFO] Programa finalizado.")
    print(f"Palabra clave detectada: {resultado}")