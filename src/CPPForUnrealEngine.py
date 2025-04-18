import customtkinter as ctk
import subprocess
import threading
import os
import webbrowser
import re
import json
from collections import defaultdict
import argparse

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
    # Regex para classes, structs, interfaces Unreal e enums
    class_pattern = re.compile(
        r'UCLASS\s*(?:\(.*?\))?\s*\n\s*class\s+(?:[A-Z_]+_API\s+)?(\w+)(?:\s*:\s*([A-Za-z0-9_:<> ,]+))?\s*\{',
        re.DOTALL | re.MULTILINE)
    struct_pattern = re.compile(
        r'USTRUCT\s*(?:\(.*?\))?\s*\n\s*struct\s+(?:[A-Z_]+_API\s+)?(\w+)(?:\s*:\s*([A-Za-z0-9_:<> ,]+))?\s*\{',
        re.DOTALL | re.MULTILINE)
    # Structs SEM macro Unreal
    struct_plain_pattern = re.compile(
        r'struct\s+(?:[A-Z_]+_API\s+)?(\w+)(?:\s*:\s*([A-Za-z0-9_:<> ,]+))?\s*\{',
        re.DOTALL | re.MULTILINE)
    # Interface Unreal
    interface_pattern = re.compile(
        r'UINTERFACE\s*(?:\(.*?\))?\s*\n\s*class\s+(?:[A-Z_]+_API\s+)?(U\w+)\s*:\s*public\s+UInterface\s*\{',
        re.DOTALL | re.MULTILINE)
    interface_impl_pattern = re.compile(
        r'class\s+(?:[A-Z_]+_API\s+)?(I\w+)\s*\{',
        re.DOTALL | re.MULTILINE)
    # Enums Unreal
    enum_pattern = re.compile(
        r'UENUM\s*(?:\(.*?\))?\s*\n\s*enum\s+(?:class\s+)?(\w+)\s*:?\s*\w*\s*\{([^}]*)\}',
        re.DOTALL | re.MULTILINE)
    # Enums C++ comuns
    enum_plain_pattern = re.compile(
        r'enum\s+(?:class\s+)?(\w+)\s*:?\s*\w*\s*\{([^}]*)\}',
        re.DOTALL | re.MULTILINE)

    classes = []
    structs = []
    enums = []
    interfaces = []
    methods = []
    attributes = []

    # Classes Unreal
    for match in class_pattern.finditer(content):
        name = match.group(1)
        parent = match.group(2) if match.lastindex and match.lastindex >= 2 else None
        classes.append((name, parent))
    # Structs Unreal
    for match in struct_pattern.finditer(content):
        name = match.group(1)
        parent = match.group(2) if match.lastindex and match.lastindex >= 2 else None
        structs.append((name, parent))
    # Structs SEM macro Unreal
    for match in struct_plain_pattern.finditer(content):
        name = match.group(1)
        parent = match.group(2) if match.lastindex and match.lastindex >= 2 else None
        structs.append((name, parent))
    # Interfaces Unreal
    for match in interface_pattern.finditer(content):
        name = match.group(1)
        interfaces.append((name, 'UInterface'))
    for match in interface_impl_pattern.finditer(content):
        name = match.group(1)
        interfaces.append((name, 'IInterface'))
    # Enums Unreal
    for match in enum_pattern.finditer(content):
        enum_name = match.group(1)
        values_block = match.group(2)
        values = [v.strip().split('=')[0].split(' ')[0] for v in values_block.split(',') if v.strip()]
        enums.append((enum_name, values))
    # Enums C++ comuns
    for match in enum_plain_pattern.finditer(content):
        enum_name = match.group(1)
        values_block = match.group(2)
        values = [v.strip().split('=')[0].split(' ')[0] for v in values_block.split(',') if v.strip()]
        enums.append((enum_name, values))

    # TODO: aprimorar extração de métodos e atributos se necessário

    return classes, structs, enums, methods, attributes

def parse_file(file_path):
    try:
        if not file_path.endswith(".h"):
            return [], [], [], [], []

        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            raw = file.read()

        cleaned = clean_header_text(raw)
        return parse_cleaned_header(cleaned)
    except Exception:
        return [], [], [], [], []

def extract_class_name(type_str):
    type_str = type_str.replace("const", "").strip()
    type_str = re.sub(r"[<>&*]", " ", type_str)
    tokens = type_str.split()
    for token in reversed(tokens):
        if token.startswith("A") or token.startswith("U"):
            return token
    return None

def classify_group_by_base(parent):
    if not parent:
        return "Others"
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

def generate_puml(project_dir, entidades_txt_path=None):
    base_path = os.path.abspath(os.path.join(project_dir, ".."))
    project_name, engine_version = get_project_info(project_dir)
    output_file = os.path.join(project_dir, f"{project_name}.puml")

    all_classes = []
    all_structs = []
    all_enums = []
    all_interfaces = []
    all_methods = []
    all_attributes = []

    files_found = 0
    files_parsed = 0
    entidades_coletadas = set()

    print(f"[DEBUG] Procurando arquivos .h em {project_dir}")
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".h"):
                files_found += 1
                file_path = os.path.join(root, file)
                print(f"[DEBUG] Processando: {file_path}")
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    cleaned = clean_header_text(content)
                    classes, structs, enums, methods, attributes = parse_cleaned_header(cleaned)
                    files_parsed += 1
                    # Coletar nomes para entidades.txt
                    for c in classes:
                        if isinstance(c, (list, tuple)) and len(c) > 0:
                            entidades_coletadas.add(c[0])
                    for s in structs:
                        if isinstance(s, (list, tuple)) and len(s) > 0:
                            entidades_coletadas.add(s[0])
                    for e in enums:
                        if isinstance(e, (list, tuple)) and len(e) > 0:
                            entidades_coletadas.add(e[0])
                    # Acumular todas as entidades extraídas de todos os arquivos
                    if classes:
                        all_classes.extend(classes)
                    if structs:
                        all_structs.extend(structs)
                    if enums:
                        all_enums.extend(enums)
                    if methods:
                        all_methods.extend(methods)
                    if attributes:
                        all_attributes.extend(attributes)
                except Exception as e:
                    print(f"[WARN] Failed to parse {file_path}: {e}")
    # Fallback defensivo: garantir que os dicionários existam antes do uso
    if 'class_attrs' not in locals() or class_attrs is None:
        class_attrs = defaultdict(list)
    if 'class_methods' not in locals() or class_methods is None:
        class_methods = defaultdict(list)

    # Mensagem explícita se nenhum arquivo .h encontrado ou processado
    if files_found == 0:
        print(f"[ERRO] Nenhum arquivo .h encontrado em {project_dir}. Nada foi processado.")
    elif files_parsed == 0:
        print(f"[ERRO] Nenhum arquivo .h pôde ser processado em {project_dir}.")

    # Geração do PUML mínimo se não houver classes válidas
    if not any([all_classes, all_structs, all_enums]):
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("@startuml\n")
            f.write(f"title {project_name} - Unreal Engine {engine_version} (sem classes válidas)\n")
            f.write("' Nenhuma classe/struct/enum válida encontrada.\n")
            f.write("@enduml\n")
        print(f"[WARN] Nenhuma classe/struct/enum válida encontrada. PUML mínimo gerado em {output_file}")
        return output_file  # Retorna imediatamente para evitar NameError

    # Color map for groups (Unreal stereotypes)
    group_colors = {
        "Actors": "#193c7c",
        "Characters": "#ff8c00",
        "Controllers": "#1f4e4e",
        "GameModes": "#3c245c",
        "Components": "#2c72a8",
        "HUD": "#1d5e3b",
        "Helpers": "#484848",
        "DataAssets": "#553300",
        "Persistence": "#006060",
        "BlueprintLibraries": "#2e003e",
        "Others": "#404040",
    }

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("@startuml\n")
        f.write("left to right direction\n")
        f.write("skinparam TitleFontColor #ffffff\n")
        f.write("skinparam ranksep 1.3\n")
        f.write("skinparam nodesep 1.0\n")
        f.write("skinparam linetype polyline\n")
        f.write("skinparam ArrowThickness 2\n")
        f.write("skinparam ArrowFontColor #ffffff\n")
        f.write("skinparam backgroundColor #1e1e1e\n")
        f.write("skinparam classBackgroundColor #3c3c3c\n")
        f.write("skinparam classBorderColor #00bfff\n")
        f.write("skinparam classFontColor #ffffff\n")
        f.write("skinparam classAttributeFontColor #ffffff\n")
        f.write("skinparam classMethodFontColor #ffffff\n")
        f.write("skinparam classArrowColor #00bfff\n")
        f.write("skinparam classAttributeIconSize 0\n")
        f.write("skinparam dpi 150\n")
        f.write("skinparam package {\n")
        f.write("  BackgroundColor #2c2c2c\n")
        f.write("  BorderColor #00bfff\n")
        f.write("  FontColor #ffffff\n")
        f.write("  BackgroundColor<<Actors>> #193c7c\n")
        f.write("  BorderColor<<Actors>> #1e90ff\n")
        f.write("  BackgroundColor<<Characters>> #ff8c00\n")
        f.write("  BorderColor<<Characters>> #ff6600\n")
        f.write("  BackgroundColor<<Controllers>> #1f4e4e\n")
        f.write("  BorderColor<<Controllers>> #00ced1\n")
        f.write("  BackgroundColor<<GameModes>> #3c245c\n")
        f.write("  BorderColor<<GameModes>> #a020f0\n")
        f.write("  BackgroundColor<<Components>> #2c72a8\n")
        f.write("  BorderColor<<Components>> #00bfff\n")
        f.write("  BackgroundColor<<HUD>> #1d5e3b\n")
        f.write("  BorderColor<<HUD>> #00ff7f\n")
        f.write("  BackgroundColor<<Helpers>> #484848\n")
        f.write("  BorderColor<<Helpers>> #aaaaaa\n")
        f.write("  BackgroundColor<<DataAssets>> #553300\n")
        f.write("  BorderColor<<DataAssets>> #ffaa00\n")
        f.write("  BackgroundColor<<Persistence>> #006060\n")
        f.write("  BorderColor<<Persistence>> #00cccc\n")
        f.write("  BackgroundColor<<BlueprintLibraries>> #2e003e\n")
        f.write("  BorderColor<<BlueprintLibraries>> #b266ff\n")
        f.write("  BackgroundColor<<Others>> #404040\n")
        f.write("  BorderColor<<Others>> #999999\n")
        f.write("}\n")
        f.write(f"title {project_name} - Unreal Engine {engine_version}\n")

        # --- Pacote de Enums (mostrar todos os enums extraídos) ---
        if all_enums:
            f.write(f'package "Enums" <<UnrealGroup>> {{\n')
            for enum_item in all_enums:
                enum_name = None
                values = []
                if isinstance(enum_item, (list, tuple)):
                    if len(enum_item) == 2 and isinstance(enum_item[1], (list, tuple)):
                        enum_name = enum_item[0]
                        values = enum_item[1]
                if not (enum_name and isinstance(values, (list, tuple))):
                    continue
                f.write(f'  enum {enum_name} <<UnrealEnum>> {{\n')
                for v in values:
                    f.write(f'    {v}\n')
                f.write('  }\n')
            f.write('}\n')

        # --- Pacote de Structs (mostrar todos os structs extraídos) ---
        if all_structs:
            f.write(f'package "Structs" <<UnrealGroup>> {{\n')
            for struct_item in all_structs:
                name = None
                parent = None
                if isinstance(struct_item, (list, tuple)):
                    name = struct_item[0]
                    if len(struct_item) > 1:
                        parent = struct_item[1]
                if not name:
                    continue
                f.write(f'  struct {name} <<UnrealStruct>> {{\n')
                # (Opcional: atributos)
                # Aqui, se desejar, pode buscar atributos por nome
                f.write('  }\n')
            f.write('}\n')

        # --- Pacote de Interfaces (opcional, caso queira exibir) ---
        if 'interfaces' in locals() and all_interfaces:
            f.write(f'package "Interfaces" <<UnrealGroup>> {{\n')
            for iface in all_interfaces:
                name = iface[0]
                f.write(f'  interface {name} <<UnrealInterface>> {{}}\n')
            f.write('}\n')

        # --- Classes e demais grupos ---
        class_groups = defaultdict(list)
        for item in all_classes:
            name = None
            parent = None
            if isinstance(item, (list, tuple)):
                name = item[0]
                if len(item) > 1:
                    parent = item[1]
            if not name:
                continue
            class_groups[classify_group_by_base(parent)].append((name, parent))
        for group, class_list in class_groups.items():
            f.write(f'package "{group}" <<UnrealGroup>> {{\n')
            for item in class_list:
                name = item[0]
                parent = item[1]
                stereotype = 'UnrealClass'
                f.write(f'  class {name} <<{stereotype}>> {{\n')
                # (Opcional: atributos e métodos)
                f.write('  }\n')
            f.write('}\n')

        f.write("@enduml\n")

    # Ao final do for, gerar entidades.txt se caminho fornecido
    if entidades_txt_path is not None:
        try:
            with open(entidades_txt_path, "w", encoding="utf-8") as ef:
                for entidade in sorted(entidades_coletadas):
                    ef.write(entidade + "\n")
            print(f"[DEBUG] Arquivo de entidades atualizado: {entidades_txt_path}")
        except Exception as e:
            print(f"[ERRO] Falha ao gerar entidades.txt: {e}")

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
    svg_file = os.path.splitext(puml_path)[0] + ".svg"
    # Caminho absoluto do plantuml.jar na pasta src
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plantuml_jar = os.path.join(script_dir, "plantuml.jar")
    try:
        subprocess.run(["java", "-jar", plantuml_jar, "-tsvg", os.path.basename(puml_path)], cwd=folder, check=True)
        if os.path.exists(svg_file):
            webbrowser.open(svg_file)
            return svg_file
        else:
            return None
    except subprocess.CalledProcessError as e:
        return None

def validate_puml_coverage(puml_path, expected_entities):
    """
    Ajustada: Agora valida se o nome da entidade está presente no PUML,
    e também verifica se há métodos/atributos dentro da definição.
    Se a entidade existir mas estiver vazia, reporta como 'sem propriedades/metodos'.
    """
    presentes = []
    ausentes = []
    sem_propriedades = []
    with open(puml_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    puml_text = ''.join(lines)
    for entidade in expected_entities:
        found = False
        has_content = False
        # Procurar struct, class ou enum
        patterns = [
            rf'(struct|class) {entidade} <<Unreal(Struct|Class)>> {{',
            rf'enum {entidade} <<UnrealEnum>> {{'
        ]
        for pattern in patterns:
            for i, line in enumerate(lines):
                if re.search(pattern, line):
                    found = True
                    # Checar se há membros dentro das chaves
                    j = i + 1
                    while j < len(lines) and not lines[j].strip().startswith('}'):  # Até fechar bloco
                        if lines[j].strip() and not lines[j].strip().startswith('//'):
                            has_content = True
                            break
                        j += 1
                    break
            if found:
                break
        if found and has_content:
            presentes.append(entidade)
        elif found:
            sem_propriedades.append(entidade)
        else:
            ausentes.append(entidade)
    print(f"[VALIDAÇÃO] Entidades presentes no PUML: {presentes}")
    print(f"[VALIDAÇÃO] Entidades presentes mas SEM propriedades/métodos: {sem_propriedades}")
    print(f"[VALIDAÇÃO] Entidades AUSENTES no PUML: {ausentes}")
    return presentes, sem_propriedades, ausentes

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gera UML para projetos Unreal Engine C++")
    parser.add_argument('--project', type=str, required=True, help='Pasta do projeto Unreal')
    parser.add_argument('--tipo', type=str, default='cpp4ue', help='Tipo de projeto (cpp4ue)')
    parser.add_argument('--valida', type=str, default=None, help='Arquivo .txt com nomes de entidades esperadas para validação')
    parser.add_argument('--entidades_txt', type=str, default=None, help='Caminho para gerar entidades.txt')
    args = parser.parse_args()

    project_dir = args.project
    tipo = args.tipo
    valida_path = args.valida
    entidades_txt_path = args.entidades_txt

    print(f"[UML] Gerando UML para C++ Unreal em {project_dir}")
    print(f"[DEBUG] Procurando arquivos .h em {project_dir}")
    puml_path = generate_puml(project_dir, entidades_txt_path)
    print(f"[UML] PUML gerado: {puml_path}")
    clean_puml(puml_path)
    print(f"[UML] PUML limpo: {puml_path}")

    # --- Validação automática, se arquivo passado ---
    if valida_path:
        with open(valida_path, 'r', encoding='utf-8') as f:
            expected_entities = [l.strip() for l in f if l.strip()]
        presentes, sem_propriedades, ausentes = validate_puml_coverage(puml_path, expected_entities)
        print(f"[VALIDAÇÃO] Entidades presentes no PUML: {presentes}")
        print(f"[VALIDAÇÃO] Entidades presentes mas SEM propriedades/métodos: {sem_propriedades}")
        print(f"[VALIDAÇÃO] Entidades AUSENTES no PUML: {ausentes}")

    render_svg(puml_path)
    print("[UML] Finalizado!")
