import os
import re
from collections import defaultdict

# Regex patterns for Python class, method, and attribute extraction
CLASS_PATTERN = re.compile(r'^class (\w+)(\(([^)]*)\))?:')
METHOD_PATTERN = re.compile(r'^\s+def (\w+)\(.*\):')
ATTRIBUTE_PATTERN = re.compile(r'^\s+self\.(\w+)\s*=')


def scan_python_files(project_dir):
    """Recursively find all .py files in the project directory."""
    py_files = []
    for root, _, files in os.walk(project_dir):
        for f in files:
            if f.endswith('.py') and not f.startswith('__'):
                py_files.append(os.path.join(root, f))
    return py_files


def extract_classes(py_file):
    """Extract classes, their methods, and attributes from a Python file."""
    classes = {}
    current_class = None
    bases = None
    with open(py_file, encoding='utf-8') as f:
        for line in f:
            class_match = CLASS_PATTERN.match(line)
            if class_match:
                current_class = class_match.group(1)
                bases = class_match.group(3)
                classes[current_class] = {
                    'methods': [],
                    'attributes': [],
                    'bases': [b.strip() for b in bases.split(',')] if bases else []
                }
                continue
            if current_class:
                method_match = METHOD_PATTERN.match(line)
                if method_match:
                    method = method_match.group(1)
                    if not method.startswith('__'):
                        classes[current_class]['methods'].append(method)
                attr_match = ATTRIBUTE_PATTERN.match(line)
                if attr_match:
                    attr = attr_match.group(1)
                    classes[current_class]['attributes'].append(attr)
    return classes


def generate_puml(project_dir):
    """Generate PlantUML file for Python project."""
    py_files = scan_python_files(project_dir)
    all_classes = {}
    file_to_classes = defaultdict(list)

    for py_file in py_files:
        classes = extract_classes(py_file)
        for cname, cdata in classes.items():
            all_classes[cname] = cdata
            file_to_classes[os.path.relpath(py_file, project_dir)].append(cname)

    output_file = os.path.join(project_dir, 'PythonProject.puml')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('@startuml\n')
        f.write('skinparam backgroundColor #23272e\n')
        f.write('skinparam defaultTextAlignment center\n')
        f.write('skinparam shadowing true\n')
        f.write('skinparam classFontColor #ffffff\n')
        f.write('skinparam classAttributeFontColor #ffffff\n')
        f.write('skinparam classMethodFontColor #ffffff\n')
        f.write('skinparam classStereotypeFontColor #ffffff\n')
        f.write('skinparam classBorderColor #4b8bbe\n')  # Python blue
        f.write('skinparam classBackgroundColor #23272e\n')
        f.write('skinparam ArrowColor #f5f5f5\n')
        f.write('left to right direction\n')
        f.write('hide empty members\n')
        f.write('title Python Project UML\n\n')

        # Color palette for grouped modules (Pythonic, visually distinct, and colorblind-friendly)
        module_colors = [
            '#4b8bbe', # Python blue
            '#ffd43b', # Python yellow
            '#306998', # dark blue
            '#e06c75', # red
            '#98c379', # green
            '#c678dd', # purple
            '#56b6c2', # cyan
            '#d19a66', # orange
            '#abb2bf', # light gray
            '#282c34', # dark gray
        ]
        module_color_map = {}
        for idx, module in enumerate(file_to_classes):
            module_color_map[module] = module_colors[idx % len(module_colors)]

        # Group by module (file) with colored backgrounds and <<PythonModule>> stereotype
        for module, classes in file_to_classes.items():
            color = module_color_map[module]
            f.write(f'package "{module}" <<PythonModule>> {{\n')
            f.write(f'  skinparam packageBackgroundColor {color}\n')
            f.write(f'  skinparam packageBorderColor {color}\n')
            for cname in classes:
                cdata = all_classes[cname]
                # Add <<PythonClass>> stereotype to every class
                f.write(f'    class {cname} <<PythonClass>> {{\n')
                for attr in cdata['attributes']:
                    f.write(f'      +{attr}\n')
                for method in cdata['methods']:
                    f.write(f'      +{method}()\n')
                f.write('    }\n')
            f.write('}\n')

        # Inheritance relations
        for cname, cdata in all_classes.items():
            for base in cdata['bases']:
                if base in all_classes:
                    f.write(f'{base} <|-- {cname}\n')

        # Add stereotypes definitions for legend/colors
        f.write('\n' +
            'hide stereotype\n'+
            'skinparam class<<PythonClass>> {\n' +
            '  BackgroundColor #23272e\n' +
            '  BorderColor #4b8bbe\n' +
            '  FontColor #ffffff\n' +
            '  AttributeFontColor #ffffff\n' +
            '  MethodFontColor #ffffff\n' +
            '  StereotypeFontColor #ffffff\n' +
            '  FontStyle bold\n' +
            '}\n' +
            'skinparam package<<PythonModule>> {\n' +
            '  FontColor #23272e\n' +
            '  FontStyle bold\n' +
            '}\n')
        f.write('@enduml\n')
    print(f"PUML generated at: {output_file}")
    return output_file

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        generate_puml(sys.argv[1])
    else:
        print("Usage: python PythonUML.py <project_dir>")
