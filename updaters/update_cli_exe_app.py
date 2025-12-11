import os

VERSION = "1.0.0"

os.system(f"pyinstaller --onefile --console --icon=assets/lehaam_icon.ico --name=\"Lehaam-v{VERSION}\" apps/cli_app.py")
#MadMad_6