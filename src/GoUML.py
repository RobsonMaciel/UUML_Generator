import os
import re
import json
from collections import defaultdict
from SVGRenderer import render_svg

def scan_go_files(project_dir):
    """Recursively find all .go files in the project directory."""
    go_files = []
    for root, _, files in os.walk(project_dir):
        for f in files:
            if f.endswith('.go'):
                go_files.append(os.path.join(root, f))
    return go_files

def extract_go_structs_and_interfaces(go_file):
    """Extract structs, interfaces, methods, and fields from a Go file."""
    structs = {}
    interfaces = {}
    with open(go_file, encoding='utf-8') as f:
        content = f.read()
        # Structs
        for match in re.finditer(r'type\s+(\w+)\s+struct\s*{([\s\S]*?)}', content):
            name = match.group(1)
            body = match.group(2)
            fields = []
            for line in body.split('\n'):
                line = line.strip()
                if line and not line.startswith('//'):
                    parts = line.split()
                    if len(parts) >= 2:
                        fields.append(parts[0])
            structs[name] = {'fields': fields}
        # Interfaces
        for match in re.finditer(r'type\s+(\w+)\s+interface\s*{([\s\S]*?)}', content):
            name = match.group(1)
            body = match.group(2)
            methods = []
            for line in body.split('\n'):
                line = line.strip()
                if line and not line.startswith('//'):
                    method_name = line.split('(')[0].strip()
                    methods.append(method_name)
            interfaces[name] = {'methods': methods}
    return structs, interfaces

def generate_uml_json(project_dir):
    """Generate a UML-compliant JSON for Go structs and interfaces."""
    go_files = scan_go_files(project_dir)
    uml_json = {
        'structs': [],
        'interfaces': [],
        'relations': []
    }
    for go_file in go_files:
        structs, interfaces = extract_go_structs_and_interfaces(go_file)
        for sname, sdata in structs.items():
            uml_json['structs'].append({'name': sname, 'fields': sdata['fields']})
        for iname, idata in interfaces.items():
            uml_json['interfaces'].append({'name': iname, 'methods': idata['methods']})
    # TODO: Detect relations (implements, embeds)
    return uml_json

def generate_puml_from_json(uml_json, project_dir=None):
    """Generate PlantUML file from Go UML JSON."""
    puml_lines = ["@startuml"]
    puml_lines.append('skinparam backgroundColor #23272e')
    puml_lines.append('skinparam classFontColor #ffffff')
    puml_lines.append('skinparam classAttributeFontColor #ffffff')
    puml_lines.append('skinparam classMethodFontColor #ffffff')
    puml_lines.append('skinparam classStereotypeFontColor #ffffff')
    puml_lines.append('skinparam classBorderColor #00add8')  # Go blue
    for struct in uml_json['structs']:
        puml_lines.append(f'class {struct["name"]} <<GoStruct>> {{')
        for field in struct['fields']:
            puml_lines.append(f'  {field}')
        puml_lines.append('}')
    for iface in uml_json['interfaces']:
        puml_lines.append(f'interface {iface["name"]} <<GoInterface>> {{')
        for method in iface['methods']:
            puml_lines.append(f'  {method}()')
        puml_lines.append('}')
    # TODO: Add relations (implements, embeds)
    puml_lines.append('@enduml')
    output_file = os.path.join(project_dir or '.', "GoProject.puml")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(puml_lines))
    return output_file

def main(project_dir):
    uml_json = generate_uml_json(project_dir)
    json_file = os.path.join(project_dir, 'Go_UML_ClassDiagram.json')
    with open(json_file, 'w', encoding='utf-8') as jf:
        json.dump(uml_json, jf, indent=2, ensure_ascii=False)
    print(f'[UML] Go UML JSON saved at: {json_file}')

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            uml_json = json.load(f)
    except Exception as e:
        print(f"[UML] Error reading Go JSON to generate PUML: {e}")
        return

    puml_path = generate_puml_from_json(uml_json, project_dir)
    print(f"[UML] Go PUML saved at: {puml_path}")

    svg = render_svg(puml_path)
    if svg:
        print(f"[UML] SVG generated: {svg}")
    else:
        print(f"[UML] SVG not generated!")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print('Usage: python GoUML.py <ProjectDir>')
