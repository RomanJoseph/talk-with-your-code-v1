import subprocess
import sys

SCRIPTS = {
    "start": "python main.py",
    "ingest": "python utils/ingest.py"
}

if len(sys.argv) < 2:
    print("Uso: python runner.py <comando> [argumentos]")
    print("Comandos disponíveis:", ", ".join(SCRIPTS.keys()))
    sys.exit(1)

command = sys.argv[1]
args = " ".join(f'"{arg}"' if " " in arg else arg for arg in sys.argv[2:])

if command in SCRIPTS:
    subprocess.run(f"{SCRIPTS[command]} {args}", shell=True)
else:
    print(f"Comando '{command}' não encontrado.")
    print("Comandos disponíveis:", ", ".join(SCRIPTS.keys()))
