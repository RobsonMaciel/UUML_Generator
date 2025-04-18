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
        ctk.CTkLabel(self.language_frame, text="Select language (if not auto-detected):").pack(pady=(0, 6))
        # Substitui botões por dropdown
        self.language_options = [lang for lang, _ in LANGUAGES]
        self.language_dropdown = ctk.CTkOptionMenu(
            self.language_frame,
            values=self.language_options,
            variable=self.language_var,
            command=self.select_language
        )
        self.language_dropdown.pack(pady=(0, 6))
        self.detect_btn = ctk.CTkButton(self, text="Detect Project Type Automatically", command=self.detect_language)
        self.detect_btn.pack(pady=(10, 0))
        self.folder_btn = ctk.CTkButton(self, text="Choose Root Folder", command=self.choose_folder)
        self.folder_btn.pack(pady=(10, 0))
        self.run_btn = ctk.CTkButton(self, text="Generate UML", command=self.run_pipeline, state="disabled")
        self.run_btn.pack(pady=(20, 0))
        # Terminal/log textbox
        self.log_box = ctk.CTkTextbox(self, width=580, height=120, wrap="word")
        self.log_box.pack(padx=10, pady=(10, 0), fill="both", expand=False)
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

    def log(self, text):
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")

    def run_pipeline(self):
        lang = self.selected_language
        folder = self.root_folder
        self.status_var.set(f"Running UML generation for {lang} in {folder}...")
        self.run_btn.configure(state="disabled")
        self.log_box.delete("1.0", "end")
        self.log(f"[UML] Running UML generation for {lang} in {folder}...")
        self.update()
        import subprocess
        import sys
        script_map = {
            "C++ for Unreal": "CPPForUnrealEngine.py",
            "C# for Unity": "CSharpForUnity.py",
            "Python": "PythonUML.py",
            # Futuramente: "C#": "CSharpDotNet.py", "Java": "Java.py", etc.
        }
        script_name = script_map.get(lang)
        if script_name:
            script_path = os.path.join(os.path.dirname(__file__), script_name)
            script_dir = os.path.dirname(script_path)
            result = subprocess.run([sys.executable, script_path, folder], capture_output=True, text=True, cwd=script_dir)
            self.log(result.stdout)
            if result.stderr:
                self.log(f"[STDERR] {result.stderr}")
            # After .puml, try to generate SVG with PlantUML if .puml exists
            puml_file = None
            if lang == "Python":
                puml_file = os.path.join(folder, "PythonProject.puml")
            elif lang == "C++ for Unreal":
                puml_file = os.path.join(folder, "UnrealProject.puml")
            elif lang == "C# for Unity":
                puml_file = os.path.join(folder, "UnityProject.puml")
            if puml_file and os.path.exists(puml_file):
                plantuml_jar = os.path.join(os.path.dirname(__file__), "plantuml.jar")
                svg_file = puml_file.replace(".puml", ".svg")
                cmd = ["java", "-jar", plantuml_jar, "-tsvg", puml_file]
                svg_result = subprocess.run(cmd, capture_output=True, text=True)
                self.log(svg_result.stdout)
                if svg_result.stderr:
                    self.log(f"[PlantUML STDERR] {svg_result.stderr}")
                if os.path.exists(svg_file):
                    os.startfile(svg_file)
                    self.status_var.set(f"SVG generated and opened: {svg_file}")
                else:
                    self.status_var.set(f"PUML generated, but SVG not found: {svg_file}")
                    self.log(f"[ERROR] SVG not generated for {puml_file}")
            else:
                self.status_var.set(f"PUML file not found for {lang}")
                self.log(f"[ERROR] PUML file not found: {puml_file}")
        else:
            self.status_var.set(f"UML generation for {lang} is not implemented yet.")
            self.log(f"[ERROR] UML generation for {lang} is not implemented yet.")
        self.run_btn.configure(state="normal")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
