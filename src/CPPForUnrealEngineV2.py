import os
import re
import json
from collections import defaultdict

"""
CPPForUnrealEngineV2.py
-----------------------
Gera JSON UML-compliant (conforme https://plantuml.com/class-diagram) de todos os headers C++ Unreal Engine do projeto.
Inclui TODOS os atributos e métodos presentes no header, respeitando visibilidade, sem depender de macros Unreal.
Apenas entidades e relações permitidas pelo PlantUML Class Diagram são consideradas.
"""

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

# --- Parsing de headers Unreal para UML JSON ---
def parse_unreal_headers_to_uml_json(project_dir):
    """
    Percorre todos os headers .h e gera um JSON UML-compliant (PlantUML class diagram):
    - classes, interfaces, enums
    - TODOS os atributos e métodos (com visibilidade)
    - relações: extends (herança), implements (interface)
    """
    classes = []
    interfaces = []
    enums = []
    header_contents = {}
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.h'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    header_contents[file] = f.read()
    for fname, content in header_contents.items():
        content_no_comments = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content_no_comments = re.sub(r'//.*', '', content_no_comments)
        # Enums
        for m in re.finditer(r'UENUM\s*\(.*?\)?\s*enum\s+class\s+(\w+)[^{]*{([^}]*)}', content_no_comments, re.DOTALL):
            name, body = m.group(1), m.group(2)
            values = [v.split()[0].replace(',', '') for v in body.splitlines() if v.strip() and not v.strip().startswith('//')]
            enums.append({'name': name, 'values': values})
        # Interfaces Unreal (UINTERFACE)
        for m in re.finditer(r'UINTERFACE\s*\(.*?\)?\s*class\s+(\w+)\s*:\s*public\s+UInterface\s*{', content_no_comments):
            interface_name = m.group(1)
            interfaces.append({'name': interface_name, 'methods': []})
        # Classes/Structs/Interfaces Unreal
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
                for j in range(1, 6):
                    if i + j >= len(lines):
                        break
                    decl_line = lines[i + j].strip()
                    decl_match = re.match(r'^(class|struct)\s+(\w+_API\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*(?:\:\s*public\s+([\w_:<> ,]+))?\s*({)?', decl_line)
                    if decl_match:
                        ctype = decl_match.group(1)
                        name = decl_match.group(3)
                        parent = decl_match.group(4) or ''
                        has_brace = decl_match.group(5) == '{'
                        k = i + j
                        if not has_brace:
                            while k + 1 < len(lines) and '{' not in lines[k]:
                                k += 1
                            while k + 1 < len(lines) and re.match(r'^[A-Z_]+\s*\(.*?\)?\s*$', lines[k+1].strip()):
                                k += 1
                            if k + 1 < len(lines) and '{' in lines[k+1]:
                                k += 1
                        # Extrai corpo da classe até '};'
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
                        # name contém o nome da classe, garantir que nunca seja alterado!
                        class_name = str(name)  # Fixar nome da classe para uso em métodos
                        # DEBUG: print para depuração do nome da classe
                        # print(f"[DEBUG] Classe detectada: {class_name}")
                        # Passagem 1: Coleta atributos (inclusive privados)
                        attributes = []
                        current_vis = 'private' if kind == 'class' else 'public'
                        for bl in body.split('\n'):
                            bl_strip = bl.strip()
                            vis_match = re.match(r'^(public|protected|private)\s*:\s*$', bl_strip)
                            if vis_match:
                                current_vis = vis_match.group(1)
                                continue
                            attr_match = re.match(r'([\w:<>]+(?:\s*\*)?)\s+([\w_]+)\s*(?:;|=|\[)', bl_strip)
                            if attr_match and '(' not in bl_strip and not bl_strip.startswith('static'):
                                attr_type = clean_type(attr_match.group(1))
                                attr_name = attr_match.group(2)
                                attributes.append({'name': attr_name, 'type': attr_type, 'visibility': current_vis})
                        # Passagem 2: Coleta métodos (inclusive overrides, construtor e visibilidade correta)
                        methods = []
                        current_vis = 'private' if kind == 'class' else 'public'
                        for bl in body.split('\n'):
                            bl_strip = bl.strip()
                            vis_match = re.match(r'^(public|protected|private)\s*:\s*$', bl_strip)
                            if vis_match:
                                current_vis = vis_match.group(1)
                                continue
                            # Regex aprimorada para métodos virtuais (com ou sem override)
                            meth_match = re.match(r'(virtual\s+)?([\w:<>]+(?:\s*\*)?)?\s*([A-Za-z_][\w]*)\s*\(([^)]*)\)\s*(const)?\s*(override)?\s*(final)?\s*(=\s*0)?\s*(\{|;)', bl_strip)
                            if meth_match:
                                is_virtual = meth_match.group(1) is not None
                                meth_type = clean_type(meth_match.group(2) or '')
                                meth_name = meth_match.group(3)
                                meth_params = clean_params(meth_match.group(4))
                                # DEBUG: print para depuração do nome do método e construtor
                                # print(f"[DEBUG] class_name: {class_name} | meth_name: {meth_name}")
                                # Corrige nome do construtor de forma robusta
                                if meth_name == class_name:
                                    methods.append({'name': class_name, 'type': class_name, 'params': meth_params, 'visibility': current_vis})
                                    continue
                                # Captura todos os métodos override Unreal (Tick, BeginPlay, etc.)
                                if meth_match.group(6) == 'override' or meth_name in [
                                    'Tick', 'BeginPlay', 'SetupPlayerInputComponent', 'GetLifetimeReplicatedProps', 'OnRep_PlayerState', 'GetAbilitySystemComponent', 'LoseBall_Implementation']:
                                    methods.append({'name': meth_name, 'type': meth_type if meth_type else class_name, 'params': meth_params, 'visibility': current_vis})
                                # Adiciona todos os métodos declarados
                                elif meth_type or meth_params or meth_name:
                                    methods.append({'name': meth_name, 'type': meth_type if meth_type else class_name, 'params': meth_params, 'visibility': current_vis})
                        # Relações UML
                        relations = []
                        if parent:
                            for p in parent.split(','):
                                relations.append({'type': 'extends', 'target': p.strip()})
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
                            classes.append(entity)  # Struct vira class UML
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
    print(f'[UML V2] UML JSON salvo em: {json_file}')

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print('Uso: python CPPForUnrealEngineV2.py <ProjectDir>')
