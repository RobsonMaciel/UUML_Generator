import os
import re
import json
from collections import defaultdict
from SVGRenderer import render_svg

def sanitize_name(name, used_names):
    """Sanitize entity names for PlantUML: avoid reserved words, duplicates, and invalid chars."""
    reserved = {
        'if', 'for', 'from', 'to', 'class', 'interface', 'enum', 'package', 'abstract', 'extends', 'implements',
        'return', 'default', 'public', 'private', 'protected', 'internal', 'static', 'void', 'new', 'null', 'true', 'false',
        'members', 'preferences', 'interfaces', 'MainApp', 'DialogHelper', 'OperationControl', 'BetterMenu', 'BetterMenuItem', 'BetterToggleMenuItem', 'from'
    }
    # Remove invalid chars, keep alphanum and _
    clean = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    # Avoid reserved words
    if clean.lower() in reserved:
        clean = f'{clean}_Entity'
    # Avoid duplicates
    base = clean
    i = 2
    while clean in used_names:
        clean = f'{base}_{i}'
        i += 1
    used_names.add(clean)
    return clean


def scan_cs_files(project_dir):
    """Recursively find all .cs files in the project directory."""
    cs_files = []
    for root, _, files in os.walk(project_dir):
        for f in files:
            if f.endswith('.cs'):
                cs_files.append(os.path.join(root, f))
    return cs_files


def extract_classes_methods_attributes(cs_file, used_names):
    """Extract classes, inheritance, interfaces, methods, and attributes from a C# file."""
    classes = {}
    relations = []
    with open(cs_file, encoding='utf-8') as f:
        content = f.read()
        # Classes & inheritance
        for match in re.finditer(r'class\s+(\w+)\s*(?::\s*([\w\s,<>]+))?', content):
            class_name = sanitize_name(match.group(1), used_names)
            bases = match.group(2)
            classes[class_name] = {'methods': [], 'attributes': [], 'bases': []}
            if bases:
                for base in [b.strip() for b in bases.split(',') if b.strip()]:
                    base_name = sanitize_name(base, used_names)
                    classes[class_name]['bases'].append(base_name)
                    relations.append({'from': class_name, 'to': base_name, 'type': 'extends'})
        # Interfaces
        for match in re.finditer(r'interface\s+(\w+)', content):
            iface_name = sanitize_name(match.group(1), used_names)
            classes[iface_name] = {'methods': [], 'attributes': [], 'is_interface': True}
        # Methods (for both classes and interfaces)
        for match in re.finditer(r'(public|private|protected|internal)?\s+([\w<>,\[\]]+)\s+(\w+)\s*\(([^)]*)\)', content):
            method_name = sanitize_name(match.group(3), used_names)
            for cname in classes:
                if method_name not in classes[cname]['methods']:
                    classes[cname]['methods'].append(method_name)
        # Attributes (only for classes)
        for match in re.finditer(r'(public|private|protected|internal)?\s+([\w<>,\[\]]+)\s+(\w+)\s*(=\s*[^;]+)?;', content):
            attr_name = sanitize_name(match.group(3), used_names)
            for cname in classes:
                if 'is_interface' not in classes[cname] and attr_name not in classes[cname]['attributes']:
                    classes[cname]['attributes'].append(attr_name)
    return classes, relations


def generate_uml_json(project_dir):
    """Generate a UML-compliant JSON for C# classes, interfaces, and relations."""
    cs_files = scan_cs_files(project_dir)
    uml_json = {
        'classes': [],
        'interfaces': [],
        'relations': []
    }
    used_names = set()
    for cs_file in cs_files:
        classes, relations = extract_classes_methods_attributes(cs_file, used_names)
        for cname, cdata in classes.items():
            if cdata.get('is_interface'):
                uml_json['interfaces'].append({'name': cname, 'methods': cdata['methods']})
            else:
                uml_json['classes'].append({'name': cname, 'methods': cdata['methods'], 'attributes': cdata['attributes'], 'bases': cdata.get('bases', [])})
        uml_json['relations'].extend(relations)
    # Detect implements (class implements interface)
    for cls in uml_json['classes']:
        for base in cls.get('bases', []):
            if any(base == iface['name'] for iface in uml_json['interfaces']):
                uml_json['relations'].append({'from': cls['name'], 'to': base, 'type': 'implements'})
    return uml_json


def generate_puml_from_json(uml_json, project_dir=None):
    """Generate PlantUML file from C# UML JSON, with improved colors and glowing arrows."""
    puml_lines = ["@startuml"]
    # Background and box style
    puml_lines.append('skinparam backgroundColor #23272e')
    puml_lines.append('skinparam classFontColor #000000')  # Black text
    puml_lines.append('skinparam classAttributeFontColor #000000')
    puml_lines.append('skinparam classMethodFontColor #000000')
    puml_lines.append('skinparam classStereotypeFontColor #000000')
    puml_lines.append('skinparam classBorderColor #178600')  # C# green
    puml_lines.append('skinparam shadowing true')
    # Glowing, vivid arrows
    puml_lines.append('skinparam ArrowColor #00ffe7')
    puml_lines.append('skinparam ArrowThickness 3')
    puml_lines.append('skinparam ArrowFontColor #00ffe7')
    puml_lines.append('skinparam ArrowFontSize 14')
    puml_lines.append('skinparam ArrowFontStyle bold')
    puml_lines.append('skinparam ArrowLollipopColor #00ffe7')
    puml_lines.append('skinparam ArrowGlowColor #00ffe7')
    puml_lines.append('skinparam ArrowGlow 0.5')
    # Interface and class definitions
    for iface in uml_json['interfaces']:
        puml_lines.append(f'interface {iface["name"]} <<CSharpInterface>> {{')
        for method in iface['methods']:
            puml_lines.append(f'  {method}()')
        puml_lines.append('}')
    for cls in uml_json['classes']:
        puml_lines.append(f'class {cls["name"]} <<CSharpClass>> {{')
        for attr in cls['attributes']:
            puml_lines.append(f'  {attr}')
        for method in cls['methods']:
            puml_lines.append(f'  {method}()')
        puml_lines.append('}')
    for rel in uml_json['relations']:
        if rel['type'] == 'extends':
            puml_lines.append(f'{rel["from"]} --|> {rel["to"]}')
        elif rel['type'] == 'implements':
            puml_lines.append(f'{rel["from"]} ..|> {rel["to"]}')
    puml_lines.append('@enduml')
    output_file = os.path.join(project_dir or '.', "CSharpProject.puml")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(puml_lines))
    return output_file


def main(project_dir):
    uml_json = generate_uml_json(project_dir)
    json_file = os.path.join(project_dir, 'CSharp_UML_ClassDiagram.json')
    with open(json_file, 'w', encoding='utf-8') as jf:
        json.dump(uml_json, jf, indent=2, ensure_ascii=False)
    print(f'[UML] CSharp UML JSON saved at: {json_file}')

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            uml_json = json.load(f)
    except Exception as e:
        print(f"[UML] Error reading CSharp JSON to generate PUML: {e}")
        return

    puml_path = generate_puml_from_json(uml_json, project_dir)
    print(f"[UML] CSharp PUML saved at: {puml_path}")

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
        print('Usage: python CSharpUML.py <ProjectDir>')
