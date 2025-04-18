import os
import re
import json
from collections import defaultdict

"""
CPPForUnrealEngine.py
-----------------------
Generates UML-compliant JSON (according to https://plantuml.com/class-diagram) for all Unreal Engine C++ headers in the project.
Includes ALL attributes and methods present in the header, respecting visibility, without depending on Unreal macros.
Only entities and relationships allowed by the PlantUML Class Diagram are considered.
"""

def clean_type(type_str):
    """
    Cleans the data type by removing unwanted characters.
    """
    type_str = re.sub(r'[&*]', '', type_str)
    type_str = re.sub(r'<[^>]*>', '', type_str)
    type_str = re.sub(r'\b(const|virtual|static|inline|override|final|explicit|friend|mutable|volatile|constexpr|typename|class|struct|enum|public|protected|private)\b', '', type_str)
    return type_str.strip()

def clean_param(param):
    """
    Cleans the parameter by removing unwanted characters.
    """
    param = clean_type(param)
    param = re.sub(r'\b\w+\s*$', '', param).strip()
    return param

def clean_params(params_str):
    """
    Cleans the parameters by removing unwanted characters.
    """
    if not params_str.strip():
        return ''
    params = []
    for p in params_str.split(','):
        p = clean_param(p.strip())
        if p:
            params.append(p)
    return ', '.join(params)

# --- Unreal header parsing to UML JSON ---
def parse_unreal_headers_to_uml_json(project_dir):
    """
    Scans all .h headers inside the Source folder and generates a UML-compliant JSON (PlantUML class diagram):
    - classes, interfaces, enums
    - ALL attributes and methods (with visibility)
    - relationships: extends (inheritance), implements (interface)
    """
    import sys
    source_dir = os.path.join(project_dir, 'Source')
    if not os.path.isdir(source_dir):
        print(f"[UML] ERROR: Could not find 'Source' folder in {project_dir}.")
        print("[UML] Please make sure you are running this in a valid Unreal Engine project root.")
        if getattr(sys, 'frozen', False):
            input('Press any key to exit...')
        sys.exit(1)
    classes = []
    interfaces = []
    enums = []
    all_class_names = set()
    header_data = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.h'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                for decl_match in re.finditer(r'class\s+(\w+)', content):
                    all_class_names.add(decl_match.group(1))
                header_data.append((file_path, content))
    if not header_data:
        print(f"[UML] ERROR: No .h files found inside the 'Source' folder: {source_dir}")
        if getattr(sys, 'frozen', False):
            input('Press any key to exit...')
        sys.exit(1)
    # Second pass: process each header normally
    for file_path, content in header_data:
        content_no_comments = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content_no_comments = re.sub(r'//.*', '', content_no_comments)
        # Enums
        for m in re.finditer(r'UENUM\s*\(.*?\)?\s*enum\s+class\s+(\w+)[^{]*{([^}]*)}', content_no_comments, re.DOTALL):
            name, body = m.group(1), m.group(2)
            values = [v.split()[0].replace(',', '') for v in body.splitlines() if v.strip() and not v.strip().startswith('//')]
            enums.append({'name': name, 'values': values})
        # Unreal Interfaces (UINTERFACE)
        for m in re.finditer(r'UINTERFACE\s*\(.*?\)?\s*class\s+(\w+)\s*:\s*public\s+UInterface\s*{', content_no_comments):
            interface_name = m.group(1)
            interfaces.append({'name': interface_name, 'methods': []})
        # Unreal Classes/Structs/Interfaces
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
                # New: join declaration lines until '{' or ':' is found
                decl_j = 1
                decl_lines = [lines[i + decl_j].strip()]
                while '{' not in decl_lines[-1] and ':' not in decl_lines[-1] and i + decl_j + 1 < len(lines):
                    decl_j += 1
                    decl_lines.append(lines[i + decl_j].strip())
                decl_line_full = ' '.join(decl_lines)
                # Robust regex for Unreal: supports macro API and inheritance
                decl_match = re.match(r'class\s+(?:\w+_API\s+)?([A-Za-z_][A-Za-z0-9_]*)\b', decl_line_full)
                if decl_match:
                    ctype = 'class'
                    name = decl_match.group(1)
                    parent = ''
                    # Try to capture inheritance if present
                    parent_match = re.search(r':\s*public\s+([\w_:<> ,]+)', decl_line_full)
                    if parent_match:
                        parent = parent_match.group(1)
                    k = i + decl_j
                    # Extract class body until '};'
                    body_lines = []
                    started = False
                    for lidx in range(k, len(lines)):
                        l = lines[lidx]
                        body_lines.append(l)
                        if '{' in l:
                            started = True
                        if started and re.search(r'}\s*;', l):
                            break
                    body = '\n'.join(body_lines)
                    class_name = str(name)
                    # Pass 1: Collect attributes (including private)
                    attributes = []
                    current_vis = 'private' if kind == 'class' else 'public'
                    for bl in body.split('\n'):
                        bl_strip = bl.strip()
                        vis_match = re.match(r'^(public|protected|private)\s*:\s*$', bl_strip)
                        if vis_match:
                            current_vis = vis_match.group(1)
                            continue
                        attr_match = re.match(r'([\w:<>]+(?:\s*\*)?)\s+([\w_]+)\s*(?:;|=|\[)', bl_strip)
                        if attr_match and '(' not in bl_strip and not bl_strip.startswith('//'):
                            attr_type = clean_type(attr_match.group(1))
                            attr_name = attr_match.group(2)
                            attributes.append({'name': attr_name, 'type': attr_type, 'visibility': current_vis})
                    # Pass 2: Collect methods (including overrides, constructor and correct visibility)
                    methods = []
                    current_vis = 'private' if kind == 'class' else 'public'
                    for bl in body.split('\n'):
                        bl_strip = bl.strip()
                        vis_match = re.match(r'^(public|protected|private)\s*:\s*$', bl_strip)
                        if vis_match:
                            current_vis = vis_match.group(1)
                            continue
                        # Improved regex for virtual methods (with or without override)
                        meth_match = re.match(r'(virtual\s+)?([\w:<>]+(?:\s*\*)?)?\s*([A-Za-z_][\w]*)\s*\(([^)]*)\)\s*(const)?\s*(override)?\s*(final)?\s*(=\s*0)?\s*(\{|;)', bl_strip)
                        if meth_match:
                            is_virtual = meth_match.group(1) is not None
                            meth_type = clean_type(meth_match.group(2) or '')
                            method_name = meth_match.group(3)
                            meth_params = clean_params(meth_match.group(4))
                            # Ignore clearly truncated methods or constructors
                            if method_name == class_name or len(method_name) <= 2 or (method_name[-1:] == class_name[-1:] and len(method_name) < len(class_name)):
                                continue
                            # Fix truncated type: if the type ends the same as the class name but is truncated, fix to class name
                            if meth_type and meth_type != class_name and meth_type.endswith(class_name[:-1]):
                                meth_type = class_name
                            # Capture all Unreal override methods (Tick, BeginPlay, etc.)
                            if meth_match.group(6) == 'override' or method_name in [
                                'Tick', 'BeginPlay', 'SetupPlayerInputComponent', 'GetLifetimeReplicatedProps', 'OnRep_PlayerState', 'GetAbilitySystemComponent', 'LoseBall_Implementation']:
                                methods.append({'name': method_name, 'type': meth_type if meth_type else class_name, 'params': meth_params, 'visibility': current_vis})
                            # Add all declared methods
                            elif meth_type or meth_params or method_name:
                                methods.append({'name': method_name, 'type': meth_type if meth_type else class_name, 'params': meth_params, 'visibility': current_vis})
                    # UML Relationships
                    relations = []
                    if parent:
                        for p in parent.split(','):
                            relations.append({'type': 'extends', 'target': p.strip()})
                    # --- Add association/use relationships ---
                    # Collect attribute and method types for relationships
                    rel_targets = set()
                    for attr in attributes:
                        if attr['type'] in all_class_names and attr['type'] != class_name:
                            rel_targets.add(attr['type'])
                    for meth in methods:
                        # Parameters can be multiple types separated by comma
                        for param_type in meth.get('params', '').split(','):
                            t = param_type.strip()
                            if t in all_class_names and t != class_name:
                                rel_targets.add(t)
                    # Add association relationships
                    for target in sorted(rel_targets):
                        relations.append({'type': 'association', 'target': target})
                    # Clean the 'target' field by removing visibility and extra spaces
                    def clean_relation_target(name):
                        return re.sub(r'^(public|protected|private)\s*:?', '', name, flags=re.IGNORECASE).strip()
                    for rel in relations:
                        rel['target'] = clean_relation_target(rel['target'])
                    entity = {
                        'name': class_name,
                        'type': kind,
                        'attributes': attributes,
                        'methods': methods,
                        'relations': relations
                    }
                    if kind == 'interface':
                        interfaces.append(entity)
                    elif kind == 'struct':
                        classes.append(entity)  # Struct becomes UML class
                    else:
                        classes.append(entity)
                    break
            i += 1
    return {'classes': classes, 'interfaces': interfaces, 'enums': enums}

def main(project_dir):
    uml_json = parse_unreal_headers_to_uml_json(project_dir)
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

    # Generate dynamic PUML from real JSON
    print("\n[UML] PUML GENERATED DYNAMICALLY FROM JSON:\n")
    puml = generate_puml_from_json(uml_json, project_dir)
    print(puml)

    # Save PUML to file
    puml_path = os.path.join(project_dir, 'UML_ClassDiagram.puml')
    with open(puml_path, 'w', encoding='utf-8') as pf:
        pf.write(puml)
    print(f"[UML] PUML saved at: {puml_path}")

    # Generate SVG from PUML
    plantuml_jar_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'plantuml.jar'))
    svg_cmd = f'java -jar "{plantuml_jar_path}" -tsvg "{puml_path}"'
    print(f"[UML] Generating SVG with: {svg_cmd}")
    os.system(svg_cmd)

    # Automatically open SVG (if possible)
    svg_path = puml_path.replace('.puml', '.svg')
    if os.path.exists(svg_path):
        print(f"[UML] Opening SVG: {svg_path}")
        import webbrowser
        webbrowser.open(svg_path)
    else:
        print(f"[UML] SVG not found: {svg_path}")


def generate_puml_from_json(uml_json, project_dir=None):
    """
    Generates dynamic PUML from real UML JSON, grouping and coloring by stereotype/type.
    Classes without relationships are grouped in 'Others'.
    Bright colored arrows and boxes with shadow.
    Adds a title with project name and Unreal version, and a fictitious class with used plugins.
    """
    def clean_relation_target(name):
        return re.sub(r'^(public|protected|private)\s*:?', '', name, flags=re.IGNORECASE).strip()

    # --- Reads .uproject if available ---
    project_name = None
    unreal_version = None
    plugins = []
    if project_dir:
        import glob
        up_files = glob.glob(os.path.join(project_dir, '*.uproject'))
        if up_files:
            with open(up_files[0], 'r', encoding='utf-8') as f:
                upjson = json.load(f)
            project_name = upjson.get('Modules', [{}])[0].get('Name')
            unreal_version = upjson.get('EngineAssociation')
            plugins = [p['Name'] for p in upjson.get('Plugins', []) if p.get('Enabled')]

    classes = uml_json.get('classes', [])
    interfaces = uml_json.get('interfaces', [])
    enums = uml_json.get('enums', [])
    all_items = []
    name_to_item = {}
    for c in classes:
        st = c.get('type', 'Class').capitalize()
        item = {'name': c['name'], 'stereotype': st, 'fields': [f"+{a['name']} : {a['type']}" for a in c.get('attributes', [])], 'methods': [f"+{m['name']}({m.get('params','')}) : {m['type']}" for m in c.get('methods', [])]}
        all_items.append(item)
        name_to_item[c['name']] = item
    for i in interfaces:
        item = {'name': i['name'], 'stereotype': 'Interface', 'fields': [], 'methods': [f"+{m['name']}({m.get('params','')}) : {m['type']}" for m in i.get('methods', [])]}
        all_items.append(item)
        name_to_item[i['name']] = item
    for e in enums:
        item = {'name': e['name'], 'stereotype': 'Enum', 'fields': e.get('values', []), 'methods': []}
        all_items.append(item)
        name_to_item[e['name']] = item
    # Relationships (inheritance, implements, association)
    relations = []
    related_names = set()
    for c in classes:
        for rel in c.get('relations', []):
            target = clean_relation_target(rel['target'])
            src = c['name']
            if rel['type'] == 'extends':
                relations.append((src, target, '<|--', 'inherits'))
            elif rel['type'] == 'implements':
                relations.append((src, target, '..|>', 'implements'))
            elif rel['type'] == 'association':
                relations.append((src, target, '-->', rel.get('label','assoc')))
            related_names.add(src)
            related_names.add(target)
    # --- Detect real entities and external references ---
    real_entities = set(item['name'] for item in all_items)
    referenced_targets = set()
    class_to_external_refs = defaultdict(set)
    for c in classes:
        for rel in c.get('relations', []):
            target = clean_relation_target(rel['target'])
            referenced_targets.add(target)
            if target not in real_entities:
                class_to_external_refs[c['name']].add(target)
    only_referenced = referenced_targets - real_entities

    # 1. Discover all unique stereotypes
    stereotypes = sorted(set(item['stereotype'] for item in all_items))
    # 2. Automatically generate colors (pastel palette)
    pastel_palette = [
        '#FFD580', '#B3E6B3', '#FFB3B3', '#B3D1FF', '#E0B3FF', '#FFF0B3', '#C6E2FF', '#FFCCE5', '#D5FFCC', '#FFDFBA'
    ]
    colors = {st: pastel_palette[i % len(pastel_palette)] for i, st in enumerate(stereotypes)}
    # 3. Dynamically build skinparam
    skinparam = '\n'.join([
        f'  BackgroundColor<<{st}>> {color}' for st, color in colors.items()
    ])
    skinparam += '\n  Shadowing true\n  ArrowColor #FF4500\n  ArrowThickness 2\n  ArrowFontColor #222\n'
    skinparam += '  nodesep 80\n  ranksep 80\n'
    skinparam += '  BackgroundColor<<ExternalReference>> #E0E0E0\n  BorderColor<<ExternalReference>> #888\n  FontColor<<ExternalReference>> #666\n  FontStyle<<ExternalReference>> italic\n'

    # 4. Diagram header
    puml = ["@startuml", ""]
    puml.append("top to bottom direction")  # Forces vertical layout
    if project_name or unreal_version:
        title = f"{project_name or ''} (Unreal Engine {unreal_version or ''})".strip()
        puml.append(f"title <size:24>{title}</size>")
        puml.append("")
    puml.append("' Dynamic color definition by stereotype, shadow, spacing and vivid arrows")
    puml.append(f"skinparam class {{\n{skinparam}\n}}\n")
    # 4b. Fictitious Plugins box
    if plugins:
        puml.append('class "Plugins Used" as PluginsUsed <<(P,orchid)>> {')
        for pl in plugins:
            puml.append(f"  {pl}")
        puml.append('}')
        puml.append("")
    # 5. Group by stereotype AND name prefix
    import collections
    def get_prefix(name):
        return name[0] if name and name[0].isalpha() else '_'
    package_names = []
    for st in stereotypes:
        items_by_prefix = collections.defaultdict(list)
        for item in all_items:
            if item['stereotype'] == st and item['name'] in related_names:
                prefix = get_prefix(item['name'])
                items_by_prefix[prefix].append(item)
        if not items_by_prefix:
            continue
        for prefix, items in sorted(items_by_prefix.items()):
            pkg_name = f"{st}s_{prefix}"  # Unique name for package
            package_names.append(pkg_name)
            puml.append(f"package \"{st}s - {prefix}*\" as {pkg_name} <<Rectangle>> {{")
            for item in items:
                kind = 'struct' if st.lower() == 'struct' else ('interface' if st.lower() == 'interface' else ('enum' if st.lower() == 'enum' else 'class'))
                stereotype_tag = f"<<{st}>>"
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
    # 6. Group Others (no relationships)
    others = [item for item in all_items if item['name'] not in related_names]
    if others:
        package_names.append('Others')
        puml.append('package "Others" as Others <<Rectangle>> {')
        for item in others:
            kind = 'struct' if item['stereotype'].lower() == 'struct' else ('interface' if item['stereotype'].lower() == 'interface' else ('enum' if item['stereotype'].lower() == 'enum' else 'class'))
            stereotype_tag = f"<<{item['stereotype']}>>"
            puml.append(f"  {kind} {item['name']} {stereotype_tag} {{")
            for f in item['fields']:
                puml.append(f"    {f}")
            if item['fields'] and item['methods']:
                puml.append("    --")
            for m in item['methods']:
                puml.append(f"    {m}")
            puml.append("  }")
        puml.append('}')
        puml.append("")
    # 7. Invisible links to force vertical alignment of packages
    for i in range(len(package_names) - 1):
        puml.append(f"{package_names[i]} --[hidden]--> {package_names[i+1]}")
    # 8. Relationships (custom colored arrows, highlighted label)
    puml.append("' --- Relationships ---")
    arrow_colors = {
        '<|--': '#FF4500;line.bold', # Bright orange, inheritance
        '..|>': '#1E90FF;line.dashed', # Bright blue, implements
        '-->': '#32CD32;line.bold', # Bright green, association
    }
    for src, tgt, arrow, label in relations:
        if tgt in only_referenced:
            continue  # Do not draw arrow to external reference
        puml.append(f"{src} {arrow} {tgt} : <b><size:16>{label}</size></b>")
    puml.append("\n@enduml")
    return '\n'.join(puml)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print('Usage: python CPPForUnrealEngine.py <ProjectDir>')
