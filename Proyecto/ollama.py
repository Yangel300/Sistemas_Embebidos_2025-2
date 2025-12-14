import requests
from pathlib import Path

# Ruta del directorio donde está este script
BASE_DIR = Path(__file__).parent

# Ruta completa al archivo objetos.txt
archivo = BASE_DIR / "objetos.txt"

# Leer archivo
with open(archivo, "r", encoding="utf-8") as f:
    objetos = f.read()

prompt = f"""
Eres un asistente. Di: "Adelante se observan estos objetos:" 
Brevemente cuenta los objetos y mencionalos en 2 lineas. 


Lista:
{objetos}
"""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "phi3:mini",
        "prompt": prompt,
        "stream": False
    }
)

print("\n--- RESPUESTA DEL MODELO ---\n")
print(response.json()["response"])





