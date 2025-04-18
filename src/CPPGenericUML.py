import os
import re
from collections import defaultdict
import json

def extract_classes_from_cpp(file_content):
    classes = {}
    enums = {}
    # Regex for class/struct with optional inheritance
    class_pattern = re.compile(r'\b(class|struct)\s+(\w+)\s*(?::\s*([\w\s:,]+))?\s*{', re.MULTILINE)
    # Regex for enums
    enum_pattern = re.compile(r'\benum\s+(class\s+)?(\w+)\s*{', re.MULTILINE)
    # Regex for templates
    template_pattern = re.compile(r'template\s*<([^>]*)>')
    # Regex for methods (very basic, ignores templates/macros)
    method_pattern = re.compile(r'(?:public:|protected:|private:)?\s*([\w:<>*&]+)\s+(\w+)\s*\(([^)]*)\)\s*(const)?\s*;')
    # Regex for static methods
    static_method_pattern = re.compile(r'static\s+([\w:<>*&]+)\s+(\w+)\s*\(([^)]*)\)\s*(const)?\s*;')
    # Regex for attributes (very basic)
    attr_pattern = re.compile(r'(?:public:|protected:|private:)?\s*([\w:<>*&]+)\s+(\w+)\s*;')
    
    for enum_match in enum_pattern.finditer(file_content):
        enum_name = enum_match.group(2)
        start = enum_match.end()
        brace_count = 1
        i = start
        while brace_count > 0 and i < len(file_content):
            if file_content[i] == '{':
                brace_count += 1
            elif file_content[i] == '}':
                brace_count -= 1
            i += 1
        enum_body = file_content[start:i]
        values = [v.strip().split('=')[0].strip() for v in enum_body.split(',') if v.strip()]
        enums[enum_name] = values

    for class_match in class_pattern.finditer(file_content):
        kind, class_name, inheritance = class_match.groups()
        start = class_match.end()
        # Find the class body (naive: count braces)
        brace_count = 1
        i = start
        while brace_count > 0 and i < len(file_content):
            if file_content[i] == '{':
                brace_count += 1
            elif file_content[i] == '}':
                brace_count -= 1
            i += 1
        class_body = file_content[start:i]
        bases = []
        if inheritance:
            bases = [b.strip().split(' ')[-1] for b in inheritance.split(',')]
        # Detect templates
        template_match = template_pattern.search(file_content, 0, class_match.start())
        template_params = template_match.group(1) if template_match else None
        # Static methods
        static_methods = [m[1] for m in static_method_pattern.findall(class_body)]
        # Regular methods
        methods = [m[1] for m in method_pattern.findall(class_body) if m[1] not in static_methods]
        # Attributes
        attributes = [a[1] for a in attr_pattern.findall(class_body)]
        classes[class_name] = {
            'kind': kind,
            'bases': bases,
            'methods': methods,
            'static_methods': static_methods,
            'attributes': attributes,
            'template': template_params,
        }
    return classes, enums

def parse_headers_to_uml_json(project_dir):
    """
    Scans all .h/.hpp headers and generates a UML-compliant JSON (PlantUML class diagram):
    - classes, structs, enums
    - ALL attributes and methods (with visibility)
    - relationships: extends (inheritance), implements (interface)
    """
    uml_json = {
        "classes": [],
        "enums": [],
        "relations": []
    }
    # Varrer arquivos .h e .hpp
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.h') or file.endswith('.hpp'):
                path = os.path.join(root, file)
                try:
                    with open(path, encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    # Regex para classes/structs
                    class_pattern = re.compile(r'\b(class|struct)\s+(\w+)\s*(?::\s*([\w\s:,]+))?\s*{', re.MULTILINE)
                    # Regex para enums
                    enum_pattern = re.compile(r'\benum\s+(class\s+)?(\w+)\s*{', re.MULTILINE)
                    # Encontrar classes/structs
                    for match in class_pattern.finditer(content):
                        kind, cname, bases_str = match.groups()
                        bases = [b.strip().split(' ')[-1] for b in bases_str.split(',')] if bases_str else []
                        # Extrair corpo da classe
                        start = match.end()
                        end = content.find('};', start)
                        class_body = content[start:end] if end != -1 else ''
                        # Extrair métodos e atributos
                        method_pattern = re.compile(r'(?:public:|protected:|private:)?\s*([\w:\u003c\u003e\*\&]+)\s+(\w+)\s*\(([^)]*)\)\s*(const)?\s*;')
                        attr_pattern = re.compile(r'(?:public:|protected:|private:)?\s*([\w:\u003c\u003e\*\&]+)\s+(\w+)\s*;')
                        static_method_pattern = re.compile(r'static\s+([\w:\u003c\u003e\*\&]+)\s+(\w+)\s*\(([^)]*)\)\s*;')
                        static_methods = [m[1] for m in static_method_pattern.findall(class_body)]
                        methods = [m[1] for m in method_pattern.findall(class_body) if m[1] not in static_methods]
                        attributes = [a[1] for a in attr_pattern.findall(class_body)]
                        uml_json["classes"].append({
                            "name": cname,
                            "kind": kind,
                            "bases": bases,
                            "methods": methods,
                            "static_methods": static_methods,
                            "attributes": attributes,
                            "template": None
                        })
                        for base in bases:
                            uml_json["relations"].append({
                                "type": "<|--",
                                "from": base,
                                "to": cname
                            })
                    # Encontrar enums
                    for ematch in enum_pattern.finditer(content):
                        _, ename = ematch.groups()
                        start = ematch.end()
                        end = content.find('};', start)
                        enum_body = content[start:end] if end != -1 else ''
                        values = [line.strip().split('=')[0].strip().split('//')[0].strip() for line in enum_body.split('\n') if line.strip() and not line.strip().startswith('//') and line.strip() != '}']
                        uml_json["enums"].append({
                            "name": ename,
                            "values": values
                        })
                except Exception as e:
                    print(f"[UML] Error reading {path}: {e}")
    return uml_json

def generate_puml_from_json(uml_json, project_dir=None):
    """
    Generates PlantUML from UML JSON (compatível com Unreal/PlantUML).
    """
    puml_lines = ["@startuml"]
    puml_lines.append('skinparam backgroundColor #23272e')
    puml_lines.append('skinparam classFontColor #ffffff')
    puml_lines.append('skinparam classAttributeFontColor #ffffff')
    puml_lines.append('skinparam classMethodFontColor #ffffff')
    puml_lines.append('skinparam classStereotypeFontColor #ffffff')
    puml_lines.append('skinparam classBorderColor #d19a66') # Orange for C++
    puml_lines.append('skinparam classBackgroundColor #23272e')
    puml_lines.append('skinparam ArrowColor #f5f5f5')
    puml_lines.append('left to right direction')
    puml_lines.append('hide empty members')
    puml_lines.append('title C++ Project UML')
    puml_lines.append('')

    # Proteção: só nomes válidos
    defined_names = set()
    for class_data in uml_json["classes"]:
        cname = class_data["name"].strip()
        if not cname or not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', cname):
            continue
        defined_names.add(cname)
        stereotype = '<<struct>>' if class_data["kind"] == 'struct' else '<<class>>'
        template = f'<{class_data["template"]}>' if class_data["template"] else ''
        puml_lines.append(f'class {cname}{template} {stereotype} {{')
        for attr in class_data["attributes"]:
            if attr.strip():
                puml_lines.append(f'  +{attr}')
        for smethod in class_data["static_methods"]:
            if smethod.strip():
                puml_lines.append(f'  {{static}} +{smethod}()')
        for method in class_data["methods"]:
            if method.strip():
                puml_lines.append(f'  +{method}()')
        puml_lines.append('}')
    for enum_data in uml_json["enums"]:
        ename = enum_data["name"].strip()
        if not ename or not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', ename):
            continue
        defined_names.add(ename)
        puml_lines.append(f'enum {ename} {{')
        for value in enum_data["values"]:
            if value.strip():
                puml_lines.append(f'  {value}')
        puml_lines.append('}')
    for relation in uml_json["relations"]:
        src = relation["from"].strip()
        tgt = relation["to"].strip()
        if src in defined_names and tgt in defined_names:
            puml_lines.append(f'{src} {relation["type"]} {tgt}')
    puml_lines.append('@enduml')
    output_file = os.path.join(project_dir or '.', "CppProject.puml")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(puml_lines))
    return output_file

from CSharpForUnity import render_svg

def main(project_dir):
    uml_json = parse_headers_to_uml_json(project_dir)
    json_file = os.path.join(project_dir, 'UML_ClassDiagram.json')
    with open(json_file, 'w', encoding='utf-8') as jf:
        json.dump(uml_json, jf, indent=2, ensure_ascii=False)
    print(f'[UML] UML JSON saved at: {json_file}')

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            uml_json = json.load(f)
    except Exception as e:
        print(f"[UML] Error reading JSON to generate PUML: {e}")
        return

    puml_path = generate_puml_from_json(uml_json, project_dir)
    print(f"[UML] PUML saved at: {puml_path}")

    svg = render_svg(puml_path)
    if svg:
        print(f"[UML] SVG generated: {svg}")
    else:
        print(f"[UML] SVG not generated!")

# Mantém o entrypoint CLI
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print('Usage: python CPPGenericUML.py <ProjectDir>')

# Exporta explicitamente para importação
__all__ = ["main"]
