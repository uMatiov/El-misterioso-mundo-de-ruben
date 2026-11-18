import json
import re
from pathlib import Path

ORIGEN = Path("borradores")
DESTINO = Path("capitulos")

def main():
    ORIGEN.mkdir(exist_ok=True)
    DESTINO.mkdir(exist_ok=True)

    archivos = sorted(list(ORIGEN.glob("*.txt")) + list(ORIGEN.glob("*.md")))
    if not archivos:
        print("Coloca archivos como 001.txt o 022.md dentro de la carpeta 'borradores/' y vuelve a ejecutar.")
        return

    for ruta in archivos:
        digitos = "".join(c for c in ruta.stem if c.isdigit())
        if not digitos:
            print(f"Saltado (sin número en el nombre): {ruta.name}")
            continue

        num_cap = int(digitos)
        num_pad = f"{num_cap:03d}"

        texto = ruta.read_text(encoding="utf-8").strip()
        parrafos = [linea.strip() for linea in texto.splitlines() if linea.strip()]

        # Si el borrador comienza con '# Título', lo quita del cuerpo para no duplicarlo
        if parrafos and re.match(r"^#\s+", parrafos[0]):
            parrafos.pop(0)

        salida_js = (
            "window.CAPITULOS_CACHE = window.CAPITULOS_CACHE || {};\n"
            f"window.CAPITULOS_CACHE[{num_cap}] = {json.dumps(parrafos, ensure_ascii=False, indent=2)};\n"
        )

        destino_archivo = DESTINO / f"{num_pad}.js"
        destino_archivo.write_text(salida_js, encoding="utf-8")
        print(f"Generado: {destino_archivo} ({len(parrafos)} párrafos)")

if __name__ == "__main__":
    main()