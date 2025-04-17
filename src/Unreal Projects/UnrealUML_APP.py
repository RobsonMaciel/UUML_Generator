import customtkinter as ctk
import subprocess
import threading
import os
import webbrowser
import re
import json
from collections import defaultdict

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def clean_header_text(text):
    text = re.sub(r"//.*", "", text)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"(?m)^\s*(public|protected|private)\s*:\s$", "", text)
    text = re.sub(r"(?m)^\s*const\s$", "", text)
    text = re.sub(r"(?m)^\s*const override\s$", "", text)
    text = re.sub(r"\b(class|struct)\s+\w+\s$", "", text, flags=re.MULTILINE)
    text = re.sub(r"(?m)^\s*$", "", text)
    return text

def parse_cleaned_header(content):
    class_regex = r"UCLASS\s*\(.*?\)\s*class\s+\w+_API\s+(\w+)\s*:\s*public\s+([\w:]+)"
    method_regex = r"(?:UFUNCTION\s*\(.*?\)\s*)?(?:(?:virtual|static|inline)\s+)*([\w:<>&*\s]+?)\s+(\w+)\s*\(([^)]*)\)\s*(?:const)?\s*(?:override)?\s*(?:final)?\s*;"
    attribute_regex = r"(?:UPROPERTY\s*\(.*?\)\s*)?([\w:<>&*]+(?:\s*<.*?>)?(?:\s*[*&])?)\s+(\w+)\s*(?:=\s*[^;]*)?\s*;"

    classes = re.findall(class_regex, content)
    methods = re.findall(method_regex, content)

    attributes = []
    for attr_type, attr_name in re.findall(attribute_regex, content):
        if not attr_type.startswith("class") and "override" not in attr_type and attr_type.strip() != "const":
            attributes.append((attr_type.strip(), attr_name.strip()))

    return classes, methods, attributes

def parse_file(file_path):
    try:
        if not file_path.endswith(".h"):
            return [], [], []

        with open(file_path, "r", encoding="utf-8") as file:
            raw = file.read()

        cleaned = clean_header_text(raw)
        return parse_cleaned_header(cleaned)
    except Exception:
        return [], [], []

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
        return "Others"

def get_project_info(base_path):
    uproject_path = next((os.path.join(base_path, f) for f in os.listdir(base_path) if f.endswith(".uproject")), None)
    if not uproject_path:
        return "Project", "Unknown"
    try:
        with open(uproject_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            name = os.path.splitext(os.path.basename(uproject_path))[0]
            version = data.get("EngineAssociation", "UnknownVersion")
            return name, version
    except:
        return "Project", "Unknown"

def generate_puml(project_dir):
    base_path = os.path.abspath(os.path.join(project_dir, ".."))
    project_name, engine_version = get_project_info(base_path)
    output_file = os.path.join(base_path, f"{project_name}.puml")

    class_groups = defaultdict(list)
    relations = set()

    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".h"):
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
        output.write("left to right direction\n")
        output.write("skinparam TitleFontColor #ffffff\n")
        output.write("skinparam ranksep 1.3\n")
        output.write("skinparam nodesep 1.0\n")
        output.write("skinparam linetype polyline\n")
        output.write("skinparam ArrowThickness 2\n")
        output.write("skinparam ArrowFontColor #ffffff\n")
        output.write("skinparam backgroundColor #1e1e1e\n")
        output.write("skinparam classBackgroundColor #3c3c3c\n")
        output.write("skinparam classBorderColor #00bfff\n")
        output.write("skinparam classFontColor #ffffff\n")
        output.write("skinparam classAttributeFontColor #ffffff\n")
        output.write("skinparam classMethodFontColor #ffffff\n")
        output.write("skinparam classArrowColor #00bfff\n")
        output.write("skinparam classAttributeIconSize 0\n")
        output.write("skinparam dpi 150\n")
        output.write("skinparam package {\n")
        output.write("  BackgroundColor #2c2c2c\n")
        output.write("  BorderColor #00bfff\n")
        output.write("  FontColor #ffffff\n")
        output.write("  BackgroundColor<<Actors>> #193c7c\n")
        output.write("  BorderColor<<Actors>> #1e90ff\n")
        output.write("  BackgroundColor<<Characters>> #ff8c00\n")
        output.write("  BorderColor<<Characters>> #ff6600\n")
        output.write("  BackgroundColor<<Controllers>> #1f4e4e\n")
        output.write("  BorderColor<<Controllers>> #00ced1\n")
        output.write("  BackgroundColor<<GameModes>> #3c245c\n")
        output.write("  BorderColor<<GameModes>> #a020f0\n")
        output.write("  BackgroundColor<<Components>> #2c72a8\n")
        output.write("  BorderColor<<Components>> #00bfff\n")
        output.write("  BackgroundColor<<HUD>> #1d5e3b\n")
        output.write("  BorderColor<<HUD>> #00ff7f\n")
        output.write("  BackgroundColor<<Helpers>> #484848\n")
        output.write("  BorderColor<<Helpers>> #aaaaaa\n")
        output.write("  BackgroundColor<<DataAssets>> #553300\n")
        output.write("  BorderColor<<DataAssets>> #ffaa00\n")
        output.write("  BackgroundColor<<Persistence>> #006060\n")
        output.write("  BorderColor<<Persistence>> #00cccc\n")
        output.write("  BackgroundColor<<BlueprintLibraries>> #2e003e\n")
        output.write("  BorderColor<<BlueprintLibraries>> #b266ff\n")
        output.write("  BackgroundColor<<Others>> #404040\n")
        output.write("  BorderColor<<Others>> #999999\n")
        output.write("}\n")
        output.write(f"title {project_name} - Unreal Engine {engine_version}\n")

        for group, class_list in class_groups.items():
            output.write(f"package \"{group}\" <<{group}>> {{\n")
            for cls, parent, attributes, methods in class_list:
                output.write(f"  class {cls} extends {parent} {{\n")
                for attr_type, attr_name in attributes:
                    output.write(f"    {attr_type} {attr_name}\n")
                for return_type, method_name, params in methods:
                    output.write(f"    {return_type} {method_name}({params})\n")
                output.write("  }\n")
            output.write("}\n")

        for frm, to in relations:
            output.write(f"{frm} --> {to} : uses\n")

        output.write("@enduml\n")

    return output_file

def clean_puml(input_path):
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    cleaned_lines = []
    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue
        if stripped.startswith("class ") and re.match(r"class\s+\w+$", stripped):
            continue
        if stripped in ["const", "const override"]:
            continue
        if "ATTRIBUTE_ACCESSORS" in stripped:
            continue
        if stripped.startswith("return "):
            continue

        cleaned_lines.append(line)

    with open(input_path, "w", encoding="utf-8") as file:
        file.writelines(cleaned_lines)

    return input_path

def find_puml_file():
    for file in os.listdir():
        if file.endswith(".puml"):
            return os.path.abspath(file)
    return None

def render_svg(puml_path):
    folder = os.path.dirname(puml_path)
    base_name = os.path.splitext(os.path.basename(puml_path))[0]
    svg_file = os.path.join(folder, f"{base_name}.svg")

    try:
        subprocess.run(["java", "-jar", "plantuml.jar", "-tsvg", os.path.basename(puml_path)], cwd=folder, check=True)
        if os.path.exists(svg_file):
            webbrowser.open(svg_file)
            return svg_file
        else:
            return None
    except subprocess.CalledProcessError as e:
        return None

class UMLRunnerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("UnrealUML - Full Execution")
        self.geometry("720x480")

        self.output_box = ctk.CTkTextbox(self, width=680, height=380, wrap="word")
        self.output_box.pack(padx=20, pady=(20, 10), expand=True, fill="both")

        self.run_button = ctk.CTkButton(self, text="Run All", command=self.run_all)
        self.run_button.pack(pady=(0, 10))

    def log(self, text):
        self.output_box.insert("end", text + "\n")
        self.output_box.see("end")

    def check_java_version(self):
        try:
            result = subprocess.run(["java", "-version"], capture_output=True, text=True)
            output = result.stderr if result.stderr else result.stdout
            version_match = re.search(r'version "(.*?)"', output)
            if version_match:
                version_str = version_match.group(1)
                major = int(version_str.split(".")[0]) if version_str.startswith("1.") else int(version_str.split(".")[0])
                self.log(f"Java detected: {version_str}")
                if major < 17:
                    self.log("Incompatible Java version (< 17). Opening link to install JDK 17...")
                    webbrowser.open("https://download.oracle.com/java/17/archive/jdk-17.0.12_windows-x64_bin.msi")
                    return False
                return True
            else:
                self.log("Could not detect Java version.")
                return False
        except FileNotFoundError:
            self.log("Java is not installed. Opening link to install JDK 17...")
            webbrowser.open("https://download.oracle.com/java/17/archive/jdk-17.0.12_windows-x64_bin.msi")
            return False

    def run_all(self):
        self.run_button.configure(state="disabled")
        self.output_box.delete("1.0", "end")

        def _run_all_logic():
            self.log("Starting full process...")
            if not self.check_java_version():
                self.log("Install JDK 17.0.12 before proceeding.")
                self.run_button.configure(state="normal")
                return

            self.log("\n1. Generating raw PUML...")
            try:
                source_path = os.path.join(os.getcwd(), "Source")
                if not os.path.exists(source_path):
                    self.log("Source folder not found.")
                    self.run_button.configure(state="normal")
                    return
                puml_file = generate_puml(source_path)
                self.log(f"PUML generated: {puml_file}")
            except Exception as e:
                self.log(f"Error generating PUML: {e}")
                self.run_button.configure(state="normal")
                return

            self.log("\n2. Cleaning PUML...")
            try:
                cleaned = clean_puml(puml_file)
                self.log(f"PUML cleaned: {cleaned}")
            except Exception as e:
                self.log(f"Error cleaning PUML: {e}")
                self.run_button.configure(state="normal")
                return

            self.log("\n3. Rendering SVG...")
            try:
                svg = render_svg(cleaned)
                if svg:
                    self.log(f"SVG generated and opened: {svg}")
                else:
                    self.log("Error: SVG not generated.")
            except Exception as e:
                self.log(f"Error rendering SVG: {e}")

            self.log("\nProcess completed successfully.")
            self.run_button.configure(state="normal")

        threading.Thread(target=_run_all_logic, daemon=True).start()

if __name__ == "__main__":
    app = UMLRunnerApp()
    app.mainloop()
