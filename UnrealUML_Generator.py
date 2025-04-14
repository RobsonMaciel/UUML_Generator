import customtkinter as ctk
from tkinter import filedialog
import subprocess
import os
import sys
import tempfile
import shutil
import webbrowser
import base64

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Base64 do generate_puml.py embutido (vai ser sobrescrito pelo PyInstaller collect process)
EMBEDDED_SCRIPT = """
aW1wb3J0IG9zCmltcG9ydCByZQppbXBvcnQgc3lzCgppZiBsZW4oc3lzLmFyZ3YpIDwgMjoKICAgIHByaW50KCJFcnJvOiBDYW1pbmhvIGRvIHByb2pldG8gbsOjbyBmb3JuZWNpZG8uIikKICAgIHN5cy5leGl0KDEpCgojIENhbWluaG8gZGEgcGFzdGEgU291cmNlIHJlY2ViaWRvIGNvbW8gYXJndW1lbnRvCnByb2plY3RfZGlyID0gb3MucGF0aC5hYnNwYXRoKHN5cy5hcmd2WzFdKQpyb290X2RpciA9IG9zLnBhdGguZGlybmFtZShwcm9qZWN0X2RpcikKCiMgRGV0ZWN0YXIgbm9tZSBkbyBwcm9qZXRvIFVucmVhbCBwZWxvIC51cHJvamVjdAp1cHJvamVjdF9uYW1lID0gTm9uZQpmb3IgZmlsZSBpbiBvcy5saXN0ZGlyKHJvb3RfZGlyKToKICAgIGlmIGZpbGUuZW5kc3dpdGgoIi51cHJvamVjdCIpOgogICAgICAgIHVwcm9qZWN0X25hbWUgPSBvcy5wYXRoLnNwbGl0ZXh0KGZpbGUpWzBdCiAgICAgICAgYnJlYWsKCmlmIG5vdCB1cHJvamVjdF9uYW1lOgogICAgcHJpbnQoIkVycm86IEFycXVpdm8gLnVwcm9qZWN0IG7Do28gZW5jb250cmFkby4iKQogICAgc3lzLmV4aXQoMSkKCm91dHB1dF9maWxlID0gb3MucGF0aC5qb2luKHJvb3RfZGlyLCBmInt1cHJvamVjdF9uYW1lfS5wdW1sIikKCiMgUmVnZXggcGFyYSBpZGVudGlmaWNhciBjbGFzc2VzLCBtw6l0b2RvcyBlIGF0cmlidXRvcwpDTEFTU19SRUdFWCA9IHIiVUNMQVNTXHMqXCguKj9cKVxzKmNsYXNzXHMrXHcrX0FQSVxzKyhcdyspXHMqOlxzKnB1YmxpY1xzKyhbXHc6XSspIgpNRVRIT0RfUkVHRVggPSByIlVGVU5DVElPTlxzKlwoLio/XClccyooPzp2aXJ0dWFsXHMrKT8oPzpbXHc6PD5cKiZdK1xzKykrKFx3KylccypcKC4qP1wpXHMqOyIKQVRUUklCVVRFX1JFR0VYID0gciJVUFJPUEVSVFlccypcKC4qP1wpXHMqKFtcdzo8PlwqJl0rKVxzKyhcdyspXHMqOyIKCmRlZiBwYXJzZV9maWxlKGZpbGVfcGF0aCk6CiAgICB0cnk6CiAgICAgICAgd2l0aCBvcGVuKGZpbGVfcGF0aCwgInIiLCBlbmNvZGluZz0idXRmLTgiKSBhcyBmaWxlOgogICAgICAgICAgICBjb250ZW50ID0gZmlsZS5yZWFkKCkKICAgICAgICBjbGFzc2VzID0gcmUuZmluZGFsbChDTEFTU19SRUdFWCwgY29udGVudCkKICAgICAgICBtZXRob2RzID0gcmUuZmluZGFsbChNRVRIT0RfUkVHRVgsIGNvbnRlbnQpCiAgICAgICAgYXR0cmlidXRlcyA9IHJlLmZpbmRhbGwoQVRUUklCVVRFX1JFR0VYLCBjb250ZW50KQogICAgICAgIHJldHVybiBjbGFzc2VzLCBtZXRob2RzLCBhdHRyaWJ1dGVzCiAgICBleGNlcHQ6CiAgICAgICAgcmV0dXJuIFtdLCBbXSwgW10KCmRlZiBnZW5lcmF0ZV9wdW1sKHByb2plY3RfZGlyKToKICAgIHB1bWwgPSBbIkBzdGFydHVtbCIsICJza2lucGFyYW0gY2xhc3NBdHRyaWJ1dGVJY29uU2l6ZSAwIl0KCiAgICBmb3Igcm9vdCwgXywgZmlsZXMgaW4gb3Mud2Fsayhwcm9qZWN0X2Rpcik6CiAgICAgICAgZm9yIGZpbGUgaW4gZmlsZXM6CiAgICAgICAgICAgIGlmIGZpbGUuZW5kc3dpdGgoIi5oIikgb3IgZmlsZS5lbmRzd2l0aCgiLmNwcCIpOgogICAgICAgICAgICAgICAgZmlsZV9wYXRoID0gb3MucGF0aC5qb2luKHJvb3QsIGZpbGUpCiAgICAgICAgICAgICAgICBjbGFzc2VzLCBtZXRob2RzLCBhdHRyaWJ1dGVzID0gcGFyc2VfZmlsZShmaWxlX3BhdGgpCgogICAgICAgICAgICAgICAgZm9yIGNscywgcGFyZW50IGluIGNsYXNzZXM6CiAgICAgICAgICAgICAgICAgICAgcHVtbC5hcHBlbmQoZiJcbmNsYXNzIHtjbHN9IGV4dGVuZHMge3BhcmVudH0ge3siKQogICAgICAgICAgICAgICAgICAgIGZvciBhdHRyX3R5cGUsIGF0dHJfbmFtZSBpbiBhdHRyaWJ1dGVzOgogICAgICAgICAgICAgICAgICAgICAgICBwdW1sLmFwcGVuZChmIiAge2F0dHJfdHlwZS5zdHJpcCgpfSB7YXR0cl9uYW1lfSIpCiAgICAgICAgICAgICAgICAgICAgZm9yIG1ldGhvZCBpbiBtZXRob2RzOgogICAgICAgICAgICAgICAgICAgICAgICBwdW1sLmFwcGVuZChmIiAge21ldGhvZH0oKSIpCiAgICAgICAgICAgICAgICAgICAgcHVtbC5hcHBlbmQoIn0iKQoKICAgIHB1bWwuYXBwZW5kKCJcbkBlbmR1bWwiKQoKICAgIHdpdGggb3BlbihvdXRwdXRfZmlsZSwgInciLCBlbmNvZGluZz0idXRmLTgiKSBhcyBmOgogICAgICAgIGYud3JpdGUoIlxuIi5qb2luKHB1bWwpKQoKICAgIHByaW50KG91dHB1dF9maWxlKSAgIyByZXRvcm5hIGNhbWluaG8gY29tcGxldG8gcGFyYSB1c28gbm8gYXBwCgpnZW5lcmF0ZV9wdW1sKHByb2plY3RfZGlyKQo=
"""

class UMLApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("UnrealUML Generator")
        self.geometry("720x240")
        self.project_path = ctk.StringVar()
        self.temp_script_path = None

        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=20, padx=20, fill="x")

        self.entry = ctk.CTkEntry(input_frame, textvariable=self.project_path, width=500)
        self.entry.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.browse_btn = ctk.CTkButton(input_frame, text="Browse", width=80, command=self.browse_folder)
        self.browse_btn.pack(side="left")

        self.generate_btn = ctk.CTkButton(self, text="Gerar Diagrama", command=self.generate_diagram)
        self.generate_btn.pack(pady=(0, 10))

        self.status_label = ctk.CTkLabel(self, text="", wraplength=680, justify="left")
        self.status_label.pack(pady=5)

        self.auto_detect_source()
        self.extract_embedded_script()

    def extract_embedded_script(self):
        try:
            decoded = base64.b64decode(EMBEDDED_SCRIPT.encode())
            temp_dir = tempfile.gettempdir()
            self.temp_script_path = os.path.join(temp_dir, "generate_puml.py")
            with open(self.temp_script_path, "wb") as f:
                f.write(decoded)
        except Exception as e:
            self.status_label.configure(text=f"Erro ao extrair o script: {e}")

    def auto_detect_source(self):
        for root, dirs, files in os.walk(os.getcwd()):
            if 'Source' in dirs:
                self.project_path.set(os.path.join(root, 'Source'))
                break

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.project_path.set(folder)

    def generate_diagram(self):
        path = self.project_path.get()
        if not os.path.isdir(path):
            self.status_label.configure(text="Caminho inválido.")
            return

        python_exec = shutil.which("python") or shutil.which("python3") or "python"

        try:
            result = subprocess.run(
                [python_exec, self.temp_script_path, path],
                capture_output=True, text=True, check=True
            )
            puml_path = os.path.abspath(result.stdout.strip())
            puml_dir = os.path.dirname(puml_path)
            puml_file = os.path.basename(puml_path)
            png_path = puml_path.replace(".puml", "_uml.png")

            self.status_label.configure(text=f"PUML gerado: {puml_path}\nGerando PNG...")

            subprocess.run(["java", "-jar", "plantuml.jar", puml_file],
                           cwd=puml_dir, check=True)

            if os.path.exists(png_path):
                self.status_label.configure(text=f"Imagem gerada com sucesso em:\n{png_path}")
                webbrowser.open(png_path)
            else:
                self.status_label.configure(text=f"Erro: imagem não encontrada em {png_path}")

        except subprocess.CalledProcessError as e:
            self.status_label.configure(text=f"Erro de execução:\n{e.stderr or str(e)}")

if __name__ == "__main__":
    app = UMLApp()
    app.mainloop()
