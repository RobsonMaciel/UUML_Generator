import os
import re
import json
from collections import defaultdict

def clean_header_text(text):
    text = re.sub(r"//.*", "", text)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"(?m)^\s*(public|protected|private)\s*:\s*$", "", text)
    text = re.sub(r"(?m)^\s*const\s*$", "", text)
    text = re.sub(r"(?m)^\s*const override\s*$", "", text)
    text = re.sub(r"\b(class|struct)\s+\w+\s*$", "", text, flags=re.MULTILINE)
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
        return "Outros"

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
        output.write("}\n")
        output.write(f"title {project_name} - Unreal Engine {engine_version}\n")

        for group, class_list in class_groups.items():
            output.write(f"package \"{group}\" {{\n")
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

    print(f"PUML bruto gerado: {output_file}")
    return output_file

if __name__ == "__main__":
    source_path = os.path.join(os.getcwd(), "Source")
    if not os.path.exists(source_path):
        print("Pasta 'Source' não encontrada.")
    else:
        generate_puml(source_path)
