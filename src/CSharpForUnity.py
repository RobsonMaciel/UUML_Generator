import os
import re
import sys
import subprocess
import webbrowser
from collections import defaultdict

def extract_classes_methods_attributes(cs_code):
    class_regex = r'class\s+(\w+)\s*:\s*MonoBehaviour'
    method_regex = r'public\s+[\w<>\[\]]+\s+(\w+)\s*\(([^)]*)\)'
    attr_regex = r'public\s+[\w<>\[\]]+\s+(\w+)\s*(=\s*[^;]+)?;'
    
    classes = re.findall(class_regex, cs_code)
    methods = re.findall(method_regex, cs_code)
    attrs = re.findall(attr_regex, cs_code)
    return classes, methods, attrs

def generate_puml(project_dir):
    output_file = os.path.join(project_dir, "UnityProject.puml")
    class_defs = defaultdict(lambda: {'methods': [], 'attrs': [], 'base': None})
    relations = set()
    type_groups = {
        'MonoBehaviour': {'color': '#4e9fff', 'classes': []},
        'ScriptableObject': {'color': '#b57bff', 'classes': []},
        'Component': {'color': '#6ee7b7', 'classes': []},
        'Other': {'color': '#ffb347', 'classes': []}
    }
    package_styles = {
        "MonoBehaviour": {"border": "#4e9fff", "background": "#4e9fff"},
        "ScriptableObject": {"border": "#b57bff", "background": "#b57bff"},
        "Other": {"border": "#ffb347", "background": "#ffb347"},
    }
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.cs'):
                path = os.path.join(root, file)
                try:
                    with open(path, encoding='utf-8', errors='ignore') as f:
                        code = f.read()
                    class_decl = re.findall(r'class\s+(\w+)\s*:\s*([\w, ]+)', code)
                    for cls, bases in class_decl:
                        base = bases.split(',')[0].strip()
                        class_defs[cls]['base'] = base
                        if base in type_groups:
                            type_groups[base]['classes'].append(cls)
                        elif base == 'MonoBehaviour':
                            type_groups['MonoBehaviour']['classes'].append(cls)
                        elif base == 'ScriptableObject':
                            type_groups['ScriptableObject']['classes'].append(cls)
                        elif base == 'Component':
                            type_groups['Component']['classes'].append(cls)
                        else:
                            type_groups['Other']['classes'].append(cls)
                        relations.add((cls, base, 'extends'))
                    classes, methods, attrs = extract_classes_methods_attributes(code)
                    for cls in classes:
                        class_defs[cls]['file'] = path
                    for m in methods:
                        class_defs[cls]['methods'].append(m[0])
                    for a in attrs:
                        class_defs[cls]['attrs'].append(a[0])
                    for a in attrs:
                        atype = a[0]
                        if atype in class_defs:
                            relations.add((cls, atype, 'uses'))
                except Exception:
                    continue
    def clean_name(name):
        return re.sub(r'[^a-zA-Z0-9_]', '', name)
    filtered_relations = []
    for src, dst, rel in relations:
        src_clean = clean_name(src)
        dst_clean = clean_name(dst)
        if src_clean and (rel != 'extends' or dst_clean):
            filtered_relations.append((src, dst, rel))
    base_visuals = [
        ('MonoBehaviour', '#4e9fff'),
        ('ScriptableObject', '#b57bff'),
        ('Component', '#6ee7b7')
    ]
    defined_classes = set()
    all_bases = set(clean_name(dst) for _, dst, rel in filtered_relations if rel == 'extends')
    all_defined = set(clean_name(cls) for cls in class_defs.keys())
    extra_bases = all_bases - all_defined - set(clean_name(b[0]) for b in base_visuals)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('@startuml\n')
        f.write('skinparam backgroundColor #1e1e1e\n')
        f.write('skinparam classAttributeIconSize 0\n')
        f.write('skinparam defaultTextAlignment center\n')
        f.write('skinparam shadowing true\n')
        f.write('skinparam classFontColor #ffffff\n')
        f.write('skinparam classAttributeFontColor #ffffff\n')
        f.write('skinparam classMethodFontColor #ffffff\n')
        f.write('skinparam classStereotypeFontColor #ffffff\n')
        f.write('skinparam classBorderColor #bbbbbb\n')
        f.write('skinparam classBackgroundColor #23272e\n')
        f.write('skinparam ArrowColor #f5f5f5\n')
        f.write('left to right direction\n')
        f.write('skinparam package<<MonoBehaviour>> {\n')
        f.write('  BorderColor #4e9fff\n')
        f.write('  BackgroundColor #4e9fff\n')
        f.write('}\n')
        f.write('skinparam package<<ScriptableObject>> {\n')
        f.write('  BorderColor #b57bff\n')
        f.write('  BackgroundColor #b57bff\n')
        f.write('}\n')
        f.write('skinparam package<<Other>> {\n')
        f.write('  BorderColor #ffb347\n')
        f.write('  BackgroundColor #ffb347\n')
        f.write('}\n')
        package_names = set()
        for ptype, info in type_groups.items():
            if info['classes']:
                pname = clean_name(ptype)
                f.write(f'package "{pname}" <<{pname}>> {{\n')
                package_names.add(pname)
                for cls in info['classes']:
                    cname = clean_name(cls)
                    if cname not in defined_classes:
                        data = class_defs.get(cls, {'attrs': [], 'methods': []})
                        if data['attrs'] or data['methods']:
                            f.write(f'    class {cname} {{\n')
                            for attr in data['attrs']:
                                f.write(f'        +{clean_name(attr)}\n')
                            for meth in data['methods']:
                                f.write(f'        +{clean_name(meth)}()\n')
                            f.write('    }\n')
                        else:
                            f.write(f'    class {cname}\n')
                        defined_classes.add(cname)
                f.write('}\n')
        for base, color in base_visuals:
            bname = clean_name(base)
            if bname not in defined_classes and bname not in package_names:
                f.write(f'abstract class {bname} <<(A,#cccccc)>>\n')
                defined_classes.add(bname)
        for base in extra_bases:
            if base and base not in defined_classes:
                f.write(f'abstract class {base} <<(A,#888888)>>\n')
                defined_classes.add(base)
        for src, dst, rel in filtered_relations:
            src_clean = clean_name(src)
            dst_clean = clean_name(dst)
            if rel == 'extends' and dst_clean:
                f.write(f'{src_clean} --|> {dst_clean}\n')
            elif rel == 'uses':
                f.write(f'{src_clean} ..> {dst_clean} : uses\n')
        f.write('@enduml\n')
    return output_file

def render_svg(puml_path):
    folder = os.path.dirname(puml_path)
    svg_file = os.path.splitext(puml_path)[0] + ".svg"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plantuml_jar = os.path.join(script_dir, "plantuml.jar")
    try:
        subprocess.run(["java", "-jar", plantuml_jar, "-tsvg", os.path.basename(puml_path)], cwd=folder, check=True)
        if os.path.exists(svg_file):
            webbrowser.open(svg_file)
            return svg_file
        else:
            return None
    except subprocess.CalledProcessError:
        return None

def main():
    if len(sys.argv) > 1:
        root_folder = sys.argv[1]
        os.chdir(root_folder)
        print(f"[UML] Running for Unity3D C# in folder: {root_folder}")
        try:
            puml_file = generate_puml(root_folder)
            print(f"[UML] PUML generated: {puml_file}")
            svg = render_svg(puml_file)
            if svg:
                print(f"[UML] SVG generated: {svg}")
            else:
                print("[UML] SVG not generated!")
                sys.exit(1)
        except Exception as e:
            print(f"[UML] Error: {e}")
            sys.exit(1)
        sys.exit(0)
    else:
        print("Please provide the project path as an argument.")

if __name__ == "__main__":
    main()
