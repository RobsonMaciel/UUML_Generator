import os
import re
from collections import defaultdict

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

def generate_puml(project_dir):
    output_file = os.path.join(project_dir, "CppProject.puml")
    all_classes = {}
    all_enums = {}
    file_to_classes = defaultdict(list)
    file_to_enums = defaultdict(list)
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.h') or file.endswith('.hpp') or file.endswith('.cpp'):
                path = os.path.join(root, file)
                try:
                    with open(path, encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    classes, enums = extract_classes_from_cpp(content)
                    for cname, cdata in classes.items():
                        all_classes[cname] = cdata
                        file_to_classes[file].append(cname)
                    for ename, values in enums.items():
                        all_enums[ename] = values
                        file_to_enums[file].append(ename)
                except Exception as e:
                    print(f"[UML] Error reading {path}: {e}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('@startuml\n')
        f.write('skinparam backgroundColor #23272e\n')
        f.write('skinparam classFontColor #ffffff\n')
        f.write('skinparam classAttributeFontColor #ffffff\n')
        f.write('skinparam classMethodFontColor #ffffff\n')
        f.write('skinparam classStereotypeFontColor #ffffff\n')
        f.write('skinparam classBorderColor #d19a66\n') # Orange for C++
        f.write('skinparam classBackgroundColor #23272e\n')
        f.write('skinparam ArrowColor #f5f5f5\n')
        f.write('left to right direction\n')
        f.write('hide empty members\n')
        f.write('title C++ Project UML\n\n')
        # Color palette for grouped modules (files)
        module_colors = [
            '#d19a66', # orange
            '#e06c75', # red
            '#56b6c2', # cyan
            '#abb2bf', # gray
            '#98c379', # green
            '#c678dd', # purple
            '#4b8bbe', # blue
        ]
        module_color_map = {}
        for idx, module in enumerate(file_to_classes):
            module_color_map[module] = module_colors[idx % len(module_colors)]
        for module, classes in file_to_classes.items():
            color = module_color_map[module]
            f.write(f'package "{module}" <<CppModule>> {{\n')
            f.write(f'  skinparam packageBackgroundColor {color}\n')
            f.write(f'  skinparam packageBorderColor {color}\n')
            # Enums first
            for ename in file_to_enums.get(module, []):
                values = all_enums[ename]
                f.write(f'    enum {ename} <<CppEnum>> {{\n')
                for v in values:
                    f.write(f'      {v}\n')
                f.write('    }\n')
            for cname in classes:
                cdata = all_classes[cname]
                stereotype = '<<struct>>' if cdata['kind'] == 'struct' else '<<CppClass>>'
                template = f'<{cdata["template"]}>' if cdata['template'] else ''
                f.write(f'    class {cname}{template} {stereotype} {{\n')
                for attr in cdata['attributes']:
                    f.write(f'      +{attr}\n')
                for smethod in cdata['static_methods']:
                    f.write(f'      {{static}} +{smethod}()\n')
                for method in cdata['methods']:
                    f.write(f'      +{method}()\n')
                f.write('    }\n')
            f.write('}\n')
        # Inheritance
        for cname, cdata in all_classes.items():
            for base in cdata['bases']:
                if base in all_classes:
                    f.write(f'{base} <|-- {cname}\n')
        # Stereotype visual
        f.write('\n' +
            'hide stereotype\n'+
            'skinparam class<<CppClass>> {\n' +
            '  BackgroundColor #23272e\n' +
            '  BorderColor #d19a66\n' +
            '  FontColor #ffffff\n' +
            '  AttributeFontColor #ffffff\n' +
            '  MethodFontColor #ffffff\n' +
            '  StereotypeFontColor #ffffff\n' +
            '  FontStyle bold\n' +
            '}\n' +
            'skinparam package<<CppModule>> {\n' +
            '  FontColor #23272e\n' +
            '  FontStyle bold\n' +
            '}\n' +
            'skinparam enum<<CppEnum>> {\n' +
            '  BackgroundColor #23272e\n' +
            '  BorderColor #e06c75\n' +
            '  FontColor #ffd43b\n' +
            '  FontStyle bold\n' +
            '}\n')
        f.write('@enduml\n')
    print(f"PUML generated at: {output_file}")
    return output_file

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        puml_path = generate_puml(sys.argv[1])
        # Gera SVG e abre automaticamente
        from CSharpForUnity import render_svg
        svg = render_svg(puml_path)
        if svg:
            print(f"[UML] SVG generated: {svg}")
        else:
            print("[UML] SVG not generated!")
    else:
        print("Usage: python CPPGenericUML.py <project_root>")
