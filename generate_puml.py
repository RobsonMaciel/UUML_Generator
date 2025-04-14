import os
import re
import sys
import json

CLASS_REGEX = r"UCLASS\s*\(.*?\)\s*class\s+\w+_API\s+(\w+)\s*:\s*public\s+([\w:]+)"
METHOD_REGEX = r"UFUNCTION\s*\(.*?\)\s*(?:virtual\s+)?(?:[\w:<>&*]+\s+)+(\w+)\s*\(.*?\)\s*;"
ATTRIBUTE_REGEX = r"UPROPERTY\s*\(.*?\)\s*([\w:<>&*]+)\s+(\w+)\s*;"

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

def generate_puml(project_dir):
    base_path = os.path.abspath(os.path.join(project_dir, ".."))
    uproject = find_uproject(base_path)
    project_name, engine_version = get_project_info(uproject) if uproject else ("Project", "Unknown")

    output_file = f"{project_name}.puml"

    puml_content = ["@startuml", "skinparam classAttributeIconSize 0"]
    puml_content.append(f"title {project_name} - Unreal Engine {engine_version}")

    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".h") or file.endswith(".cpp"):
                file_path = os.path.join(root, file)
                classes, methods, attributes = parse_file(file_path)
                for cls, parent in classes:
                    puml_content.append(f"\nclass {cls} extends {parent} {{")
                    for attr_type, attr_name in attributes:
                        puml_content.append(f"  {attr_type.strip()} {attr_name}")
                    for method in methods:
                        puml_content.append(f"  {method}()")
                    puml_content.append("}")

    puml_content.append("\n@enduml")

    with open(output_file, "w", encoding="utf-8") as output:
        output.write("\n".join(puml_content))

    print(output_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python generate_puml.py <caminho_para_pasta_Source>")
        sys.exit(1)

    source_dir = sys.argv[1]
    generate_puml(source_dir)
