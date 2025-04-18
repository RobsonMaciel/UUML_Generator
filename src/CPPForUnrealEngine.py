import os
import re
import json
from collections import defaultdict

def clean_type(type_str):
    type_str = re.sub(r'[&*]', '', type_str)
    type_str = re.sub(r'<[^>]*>', '', type_str)
    type_str = re.sub(r'\b(const|virtual|static|inline|override|final|explicit|friend|mutable|volatile|constexpr|typename|class|struct|enum|public|protected|private)\b', '', type_str)
    return type_str.strip()

def clean_param(param):
    param = clean_type(param)
    param = re.sub(r'\b\w+\s*$', '', param).strip()
    return param

def clean_params(params_str):
    if not params_str.strip():
        return ''
    params = []
    for p in params_str.split(','):
        p = clean_param(p.strip())
        if p:
            params.append(p)
    return ', '.join(params)

def parse_unreal_headers_to_uml_json(project_dir):
    classes = []
    interfaces = []
    enums = []
    all_class_names = set()
    header_data = []
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.h'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                for decl_match in re.finditer(r'class\s+(\w+)', content):
                    all_class_names.add(decl_match.group(1))
                header_data.append((file_path, content))
    for file_path, content in header_data:
        content_no_comments = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content_no_comments = re.sub(r'//.*', '', content_no_comments)
        for m in re.finditer(r'UENUM\s*\(.*?\)?\s*enum\s+class\s+(\w+)[^{]*{([^}]*)}', content_no_comments, re.DOTALL):
            name, body = m.group(1), m.group(2)
            values = [v.split()[0].replace(',', '') for v in body.splitlines() if v.strip() and not v.strip().startswith('//')]
            enums.append({'name': name, 'values': values})
        for m in re.finditer(r'UINTERFACE\s*\(.*?\)?\s*class\s+(\w+)\s*:\s*public\s+UInterface\s*{', content_no_comments):
            interface_name = m.group(1)
            interfaces.append({'name': interface_name, 'methods': []})
        lines = content_no_comments.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            kind = None
            if re.match(r'^UCLASS\b', line):
                kind = 'class'
            elif re.match(r'^USTRUCT\b', line):
                kind = 'struct'
            elif re.match(r'^UINTERFACE\b', line):
                kind = 'interface'
            if kind:
                decl_j = 1
                decl_lines = [lines[i + decl_j].strip()]
                while '{' not in decl_lines[-1] and ':' not in decl_lines[-1] and i + decl_j + 1 < len(lines):
                    decl_j += 1
                    decl_lines.append(lines[i + decl_j].strip())
                decl_line_full = ' '.join(decl_lines)
                m = re.match(r'(class|struct|interface)\s+(\w+)(\s*:\s*public\s+([\w\s,]+))?', decl_line_full)
                if m:
                    name = m.group(2)
                    base = m.group(4) if m.group(4) else None
                    if kind == 'class':
                        classes.append({'name': name, 'fields': [], 'methods': [], 'base': base})
                    elif kind == 'struct':
                        classes.append({'name': name, 'fields': [], 'methods': [], 'base': base, 'stereotype': 'struct'})
                    elif kind == 'interface':
                        interfaces.append({'name': name, 'methods': []})
            i += 1
    uml_json = {'classes': classes, 'interfaces': interfaces, 'enums': enums}
    return uml_json

def main(project_dir):
    uml_json = parse_unreal_headers_to_uml_json(project_dir)
    with open(os.path.join(project_dir, 'UML_ClassDiagram.json'), 'w', encoding='utf-8') as f:
        json.dump(uml_json, f, indent=2)
    puml = generate_puml_from_json(uml_json, project_dir)
    with open(os.path.join(project_dir, 'UML_ClassDiagram.puml'), 'w', encoding='utf-8') as f:
        f.write(puml)

def generate_puml_from_json(uml_json, project_dir=None):
    stereotypes = ['Class', 'Struct', 'Enum', 'Interface']
    all_items = []
    name_to_item = {}
    classes = uml_json.get('classes', [])
    interfaces = uml_json.get('interfaces', [])
    enums = uml_json.get('enums', [])
    for i in classes:
        item = {'name': i['name'], 'stereotype': i.get('stereotype', 'Class').capitalize(), 'fields': i.get('fields', []), 'methods': i.get('methods', [])}
        all_items.append(item)
        name_to_item[i['name']] = item
    for e in enums:
        item = {'name': e['name'], 'stereotype': 'Enum', 'fields': [], 'methods': [], 'values': e.get('values', [])}
        all_items.append(item)
        name_to_item[e['name']] = item
    relations = []
    only_referenced = set()
    class_to_external_refs = defaultdict(set)
    project_name = None
    unreal_version = None
    plugins = []
    skinparam = """
    BackgroundColor<<Class>> #FFD580
    BackgroundColor<<Enum>> #B3E6B3
    BackgroundColor<<Interface>> #FFB3B3
    Shadowing true
    ArrowColor #FF4500
    ArrowThickness 2
    ArrowFontColor #222
    nodesep 80
    ranksep 80
    BackgroundColor<<ExternalReference>> #E0E0E0
    BorderColor<<ExternalReference>> #888
    FontColor<<ExternalReference>> #666
    FontStyle<<ExternalReference>> italic
    """
    def get_prefix(name):
        return name[0] if name and name[0].isalpha() else '_'
    package_names = []
    if 'enums' in uml_json:
        for enum in uml_json['enums']:
            all_items = [item for item in all_items if item['name'] != enum['name']]
            all_items.append({
                'name': enum['name'],
                'stereotype': 'Enum',
                'fields': [],
                'methods': [],
                'values': enum.get('values', [])
            })
    puml = ["@startuml", ""]
    puml.append("top to bottom direction")
    puml.append(f"skinparam class {{\n{skinparam}\n}}\n")
    for st in stereotypes:
        import collections
        items_by_prefix = collections.defaultdict(list)
        for item in all_items:
            if item['stereotype'] == st:
                prefix = get_prefix(item['name'])
                items_by_prefix[prefix].append(item)
        if not items_by_prefix:
            continue
        for prefix, items in sorted(items_by_prefix.items()):
            pkg_name = f"{st}s_{prefix}"
            package_names.append(pkg_name)
            puml.append(f"package \"{st}s - {prefix}*\" as {pkg_name} <<Rectangle>> {{")
            for item in items:
                kind = 'struct' if st.lower() == 'struct' else ('interface' if st.lower() == 'interface' else ('enum' if st.lower() == 'enum' else 'class'))
                stereotype_tag = f"<<{st}>>"
                if kind == 'enum':
                    values = item.get('values')
                    if not values and 'fields' in item:
                        values = [f.split(':')[0].strip() for f in item['fields'] if f.strip()]
                    puml.append(f"  enum {item['name']} {stereotype_tag} {{")
                    if values:
                        for val in values:
                            puml.append(f"    {val}")
                    puml.append("  }")
                else:
                    puml.append(f"  {kind} {item['name']} {stereotype_tag} {{")
                    for f in item['fields']:
                        puml.append(f"    {f}")
                    if item['fields'] and item['methods']:
                        puml.append("    --")
                    for m in item['methods']:
                        puml.append(f"    {m}")
                    refs = class_to_external_refs.get(item['name'])
                    if refs:
                        puml.append("    --")
                        puml.append(f"    <<References: {', '.join(sorted(refs))}>>")
                    puml.append("  }")
            puml.append("}")
            puml.append("")
    for i in range(len(package_names) - 1):
        puml.append(f"{package_names[i]} --[hidden]--> {package_names[i+1]}")
    puml.append("' --- Relações ---")
    arrow_colors = {
        '<|--': '#FF4500;line.bold',
        '..|>': '#1E90FF;line.dashed',
        '-->': '#32CD32;line.bold',
    }
    for src, tgt, arrow, label in relations:
        if tgt in only_referenced:
            continue
        puml.append(f"{src} {arrow} {tgt} : <b><size:16>{label}</size></b>")
    puml.append("\n@enduml")
    return '\n'.join(puml)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print('Uso: python CPPForUnrealEngineV2.py <ProjectDir>')
