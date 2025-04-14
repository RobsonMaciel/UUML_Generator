import os
import re
import sys
import json
import subprocess
import webbrowser
import shutil
import customtkinter as ctk
from tkinter import filedialog
from collections import defaultdict

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

CLASS_REGEX = r"UCLASS\s*\(.*?\)\s*class\s+\w+_API\s+(\w+)\s*:\s*public\s+([\w:]+)"
METHOD_REGEX = r"(?:UFUNCTION\s*\(.*?\)\s*)?(?:virtual\s+)?(?:[\w:<>&*]+\s+)+(\w+)\s*\(.*?\)\s*;"
ATTRIBUTE_REGEX = r"(?:UPROPERTY\s*\(.*?\)\s*)?([\w:<>&*]+)\s+(\w+)\s*;"

def parse_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        classes = re.findall(CLASS_REGEX, content)
        methods = re.findall(METHOD_REGEX, content)
        attributes = re.findall(ATTRIBUTE_REGEX, content)
        return classes, methods, attributes
    except Exception:
        return [], [], []

def find_uproject(base_path):
    for file in os.listdir(base_path):
        if file.endswith(".uproject"):
            return os.path.join(base_path, file)
    return None

def get_project_info(uproject_path):
    try:
        with open(uproject_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            name = os.path.splitext(os.path.basename(uproject_path))[0]
            version = data.get("EngineAssociation", "UnknownVersion")
            return name, version
    except:
        return "Project", "UnknownVersion"

def extract_class_name(type_str):
    type_str = type_str.replace("const", "").strip()
    type_str = re.sub(r"[<>&*]", " ", type_str)
    tokens = type_str.split()
    for token in reversed(tokens):
        if token.startswith("A") or token.startswith("U"):
            return token
    return None

def classify_group_by_base(parent):
    parent = parent.replace("public ", "").replace("virtual ", "")
    if "GameMode" in parent:
        return "GameModes"
    elif "Character" in parent:
        return "Characters"
    elif "HUD" in parent:
        return "HUD"
    elif "Controller" in parent:
        return "Controllers"
    elif "Component" in parent:
        return "Components"
    elif "Library" in parent:
        return "BlueprintLibraries"
    elif "SaveGame" in parent:
        return "Persistence"
    elif "DataAsset" in parent or "Asset" in parent:
        return "DataAssets"
    elif "Actor" in parent:
        return "Actors"
    elif "Object" in parent:
        return "Helpers"
    else:
        return "Outros"

def generate_puml(project_dir):
    base_path = os.path.abspath(os.path.join(project_dir, ".."))
    uproject = find_uproject(base_path)
    project_name, engine_version = get_project_info(uproject) if uproject else ("Project", "Unknown")
    output_file = os.path.join(base_path, f"{project_name}.puml")

    class_groups = defaultdict(list)
    relations = set()

    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".h") or file.endswith(".cpp"):
                file_path = os.path.join(root, file)
                classes, methods, attributes = parse_file(file_path)

                for cls, parent in classes:
                    group_name = classify_group_by_base(parent)
                    class_groups[group_name].append((cls, parent, attributes, methods))

                    for attr_type, _ in attributes:
                        related = extract_class_name(attr_type)
                        if related and related != cls:
                            relations.add((cls, related))

    with open(output_file, "w", encoding="utf-8") as output:
        output.write("@startuml\n")
        output.write("top to bottom direction\n")
        output.write("skinparam backgroundColor #1e1e1e\n")  # Fundo escuro
        output.write("skinparam classBackgroundColor #3c3c3c\n")  # Fundo das classes
        output.write("skinparam classBorderColor #00bfff\n")  # Borda das classes (azul claro)
        output.write("skinparam classFontColor #ffffff\n")  # Texto das classes (branco)
        output.write("skinparam classAttributeFontColor #ffffff\n")  # Texto dos atributos em branco
        output.write("skinparam classMethodFontColor #ffffff\n")  # Texto dos métodos em branco
        output.write("skinparam classArrowColor #00bfff\n")  # Cor das setas (azul claro)
        output.write("skinparam packageBorderColor #00bfff\n")  # Borda dos pacotes (azul claro)
        output.write("skinparam packageBackgroundColor #2c2c2c\n")  # Fundo dos pacotes
        output.write("skinparam packageFontColor #ffffff\n")  # Texto dos pacotes (branco)
        output.write("skinparam classAttributeIconSize 0\n")  # Tamanho do ícone de atributos
        output.write("skinparam dpi 150\n")  # Resolução do diagrama
        output.write("skinparam linetype ortho\n")  # Linhas ortogonais
        output.write("skinparam shadowing true\n")  # Com sombras
        output.write("skinparam titleFontColor #ffffff\n")  # Título em branco
        output.write("skinparam arrowFontColor #ffffff\n")  # Texto das setas em branco
        output.write("skinparam stereotypeFontColor #ffffff\n")  # Texto dos estereótipos em branco
        output.write("skinparam noteFontColor #ffffff\n")  # Texto das notas em branco
        output.write("skinparam noteBackgroundColor #3c3c3c\n")  # Fundo das notas
        output.write("skinparam noteBorderColor #00bfff\n")  # Borda das notas
        output.write("skinparam shadowColor #000000\n")  # Cor da sombra
        output.write("skinparam stereotypeABackgroundColor #3c3c3c\n")  # Fundo dos estereótipos A
        output.write("skinparam stereotypeCBackgroundColor #3c3c3c\n")  # Fundo dos estereótipos C
        output.write("skinparam stereotypeEBackgroundColor #3c3c3c\n")  # Fundo dos estereótipos E
        output.write("skinparam stereotypeIBackgroundColor #3c3c3c\n")  # Fundo dos estereótipos I
        output.write(f"title {project_name} - Unreal Engine {engine_version}\n")

        for group, class_list in class_groups.items():
            output.write(f"package \"{group}\" {{\n")
            for cls, parent, attributes, methods in class_list:
                output.write(f"  class {cls} extends {parent} {{\n")
                for attr_type, attr_name in attributes:
                    output.write(f"    {attr_type.strip()} {attr_name}\n")
                for method in methods:
                    output.write(f"    {method}()\n")
                output.write("  }\n")
            output.write("}\n")

        for frm, to in relations:
            output.write(f"{frm} --> {to} : uses\n")

        output.write("@enduml\n")

    return output_file

def render_svg(puml_path):
    folder = os.path.dirname(puml_path)
    name = os.path.splitext(os.path.basename(puml_path))[0]
    subprocess.run(["java", "-jar", "plantuml.jar", "-tsvg", os.path.basename(puml_path)], cwd=folder, check=True)

    svg_path = os.path.join(folder, f"{name}.svg")
    svg_target = os.path.join(folder, f"{name}.svg")

    if os.path.exists(svg_path):
        os.replace(svg_path, svg_target)

    return svg_target

class UMLApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("UnrealUML Generator")
        self.geometry("720x240")
        self.project_path = ctk.StringVar()

        self.build_ui()
        self.auto_detect_source()

    def build_ui(self):
        frame = ctk.CTkFrame(self)
        frame.pack(pady=20, padx=20, fill="x")

        self.entry = ctk.CTkEntry(frame, textvariable=self.project_path, width=500)
        self.entry.pack(side="left", expand=True, fill="x", padx=(0, 10))

        ctk.CTkButton(frame, text="Browse", command=self.browse_folder).pack(side="left")

        ctk.CTkButton(self, text="Gerar Diagrama", command=self.generate_diagram).pack(pady=(0, 10))
        self.status_label = ctk.CTkLabel(self, text="", wraplength=680, justify="left")
        self.status_label.pack(pady=5)

    def auto_detect_source(self):
        for root, dirs, _ in os.walk(os.getcwd()):
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
        try:
            puml = generate_puml(path)
            svg = render_svg(puml)
            if os.path.exists(svg):
                self.status_label.configure(text=f"SVG gerado com sucesso:\n{svg}")
                webbrowser.open(svg)
            else:
                self.status_label.configure(text="Erro: SVG não encontrado.")
        except subprocess.CalledProcessError as e:
            self.status_label.configure(text=f"Erro ao gerar SVG: {e}")
        except Exception as e:
            self.status_label.configure(text=f"Erro inesperado: {e}")

if __name__ == "__main__":
    app = UMLApp()
    app.mainloop()