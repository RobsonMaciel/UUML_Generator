import customtkinter as ctk
from tkinter import filedialog
import subprocess
import os
import shutil
import webbrowser
from PIL import Image, ImageTk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class UMLApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("UnrealUML Generator")
        self.geometry("720x560")
        self.project_path = ctk.StringVar()

        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=20, padx=20, fill="x")

        self.entry = ctk.CTkEntry(input_frame, textvariable=self.project_path, width=500)
        self.entry.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.browse_btn = ctk.CTkButton(input_frame, text="Browse", width=80, command=self.browse_folder)
        self.browse_btn.pack(side="left")

        self.generate_btn = ctk.CTkButton(self, text="Gerar Diagrama", command=self.generate_diagram)
        self.generate_btn.pack(pady=(0, 10))

        self.status_label = ctk.CTkLabel(self, text="Prévia do Diagrama aparecerá aqui")
        self.status_label.pack(pady=5)

        self.image_label = ctk.CTkLabel(self, text="")
        self.image_label.pack(pady=10)

        self.auto_detect_source()

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
                [python_exec, "generate_puml.py", path],
                capture_output=True, text=True, check=True
            )
            puml_filename = result.stdout.strip()
            png_filename = puml_filename.replace(".puml", ".png")

            self.status_label.configure(text=f"PUML gerado: {puml_filename}")

            subprocess.run(["java", "-jar", "plantuml.jar", puml_filename], check=True)

            if os.path.exists(png_filename):
                self.status_label.configure(text=f"Imagem gerada: {png_filename}")
                try:
                    img = Image.open(png_filename)
                    img = img.resize((680, 360))
                    photo = ImageTk.PhotoImage(img)
                    self.image_label.configure(image=photo, text="")
                    self.image_label.image = photo
                except:
                    self.status_label.configure(text="Imagem pronta. Abrindo em visualizador externo...")
                    webbrowser.open(png_filename)
            else:
                self.status_label.configure(text="Erro ao gerar imagem.")
        except subprocess.CalledProcessError as e:
            self.status_label.configure(text=f"Erro: {e.stderr or str(e)}")

if __name__ == "__main__":
    app = UMLApp()
    app.mainloop()
