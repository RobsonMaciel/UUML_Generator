import customtkinter as ctk
import os
import tkinter.filedialog
import tkinter.messagebox
from typing import Optional

LANGUAGES = [
    ("C#", [".cs"]),
    ("Java", [".java"]),
    ("C++", [".cpp", ".h", ".hpp", ".cc", ".cxx"]),
    ("C++ for Unreal", [".h", ".cpp"]),
    ("C# for Unity", [".cs"]),
    ("Python", [".py"]),
]

PROJECT_SIGNATURES = {
    "C# for Unity": ["UnityEngine", "MonoBehaviour"],
    "C++ for Unreal": ["UCLASS", ".uproject"],
    # Adicione mais padrões se quiser
}

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Uuml Central App")
        self.geometry("600x400")

        self.language_var = ctk.StringVar(value="")
        self.status_var = ctk.StringVar(value="Ready.")
        self.project_path_var = ctk.StringVar(value="Project path: -")
        self.selected_language: Optional[str] = None
        self.root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        ctk.CTkLabel(self, text="Uuml – UML Generator", font=("Segoe UI", 24, "bold")).pack(pady=(20, 10))
        self.project_path_label = ctk.CTkLabel(self, textvariable=self.project_path_var, font=("Segoe UI", 12, "italic"))
        self.project_path_label.pack(pady=(0, 6))
        self.language_frame = ctk.CTkFrame(self)
        self.language_frame.pack(pady=10)
        self.lang_buttons = []
        ctk.CTkLabel(self.language_frame, text="Select language (if not auto-detected):").pack(pady=(0, 6))
        for lang, _ in LANGUAGES:
            btn = ctk.CTkButton(self.language_frame, text=lang, command=lambda l=lang: self.select_language(l))
            btn.pack(side="left", padx=5)
            self.lang_buttons.append(btn)
        self.detect_btn = ctk.CTkButton(self, text="Detect Project Type Automatically", command=self.detect_language)
        self.detect_btn.pack(pady=(10, 0))
        self.folder_btn = ctk.CTkButton(self, text="Choose Root Folder", command=self.choose_folder)
        self.folder_btn.pack(pady=(10, 0))
        self.run_btn = ctk.CTkButton(self, text="Generate UML", command=self.run_pipeline, state="disabled")
        self.run_btn.pack(pady=(20, 0))
        self.status_label = ctk.CTkLabel(self, textvariable=self.status_var)
        self.status_label.pack(side="bottom", pady=10)

    def choose_folder(self):
        folder = tkinter.filedialog.askdirectory(initialdir=self.root_folder, title="Select Root Folder")
        if folder:
            self.root_folder = folder
            self.status_var.set(f"Root folder: {folder}")
            self.project_path_var.set(f"Project path: {folder}")
            self.run_btn.configure(state="disabled")
            self.selected_language = None
            self.detect_language()  # Detecta automaticamente após escolher

    def select_language(self, lang):
        self.selected_language = lang
        self.status_var.set(f"Selected language: {lang}")
        self.project_path_var.set(f"Project path: {self.root_folder}")
        self.run_btn.configure(state="normal")

    def detect_language(self):
        detected = self._auto_detect_language()
        if detected:
            self.selected_language = detected
            self.status_var.set(f"Detected: {detected}")
            self.project_path_var.set(f"Project path: {self.root_folder}")
            self.run_btn.configure(state="normal")
        else:
            tkinter.messagebox.showinfo("Detection", "Could not automatically detect project type. Please select manually.")

    def _auto_detect_language(self) -> Optional[str]:
        # Check for project signatures
        for lang, sigs in PROJECT_SIGNATURES.items():
            for root, dirs, files in os.walk(self.root_folder):
                for file in files:
                    if any(sig in file for sig in sigs):
                        return lang
                    try:
                        with open(os.path.join(root, file), encoding="utf-8", errors="ignore") as f:
                            content = f.read(800)
                            if any(sig in content for sig in sigs):
                                return lang
                    except Exception:
                        continue
        # Fallback: check file extensions
        ext_count = {lang: 0 for lang, _ in LANGUAGES}
        for root, dirs, files in os.walk(self.root_folder):
            for file in files:
                for lang, exts in LANGUAGES:
                    if any(file.endswith(ext) for ext in exts):
                        ext_count[lang] += 1
        likely = max(ext_count, key=lambda k: ext_count[k])
        return likely if ext_count[likely] > 0 else None

    def run_pipeline(self):
        lang = self.selected_language
        folder = self.root_folder
        self.status_var.set(f"Running UML generation for {lang} in {folder}...")
        self.update()
        import subprocess
        import sys
        script_map = {
            "C++ for Unreal": "CPPForUnrealEngine.py",
            # Futuramente: "C#": "CSharpDotNet.py", "Java": "Java.py", etc.
        }
        script_name = script_map.get(lang)
        if script_name:
            script_path = os.path.join(os.path.dirname(__file__), script_name)
            if not os.path.isfile(script_path):
                self.status_var.set(f"Script for {lang} not found: {script_path}")
                return
            try:
                # Passa o root folder como argumento para o script
                result = subprocess.run([sys.executable, script_path, folder], cwd=os.path.dirname(script_path), capture_output=True, text=True)
                if result.returncode == 0:
                    self.status_var.set(f"UML generation for {lang} completed.")
                else:
                    self.status_var.set(f"Error running {script_name}: {result.stderr}")
            except Exception as e:
                self.status_var.set(f"Failed to run {script_name}: {e}")
        else:
            self.status_var.set(f"UML generation for {lang} is not implemented yet.")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
