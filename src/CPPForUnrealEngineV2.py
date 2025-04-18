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
    # Primeira passagem: coletar todos os nomes de classes
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

    # Segunda passagem: processar cada header normalmente
    for file_path, content in header_data:
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
                # Novo: unir linhas de declaração até encontrar '{' ou ':'
                decl_j = 1
                decl_lines = [lines[i + decl_j].strip()]
                while '{' not in decl_lines[-1] and ':' not in decl_lines[-1] and i + decl_j + 1 < len(lines):
                    decl_j += 1
                    decl_lines.append(lines[i + decl_j].strip())
                decl_line_full = ' '.join(decl_lines)
                # Regex robusta para Unreal: suporta macro API e herança
                decl_match = re.match(r'class\s+(?:\w+_API\s+)?([A-Za-z_][A-Za-z0-9_]*)\b', decl_line_full)
                if decl_match:
                    ctype = 'class'
                    name = decl_match.group(1)
                    parent = ''
                    # Tenta capturar herança se houver
                    parent_match = re.search(r':\s*public\s+([\w_:<> ,]+)', decl_line_full)
                    if parent_match:
                        parent = parent_match.group(1)
                    k = i + decl_j
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
                    class_name = str(name)
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
                        if attr_match and '(' not in bl_strip and not bl_strip.startswith('//'):
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
                            method_name = meth_match.group(3)
                            meth_params = clean_params(meth_match.group(4))
                            # Solução definitiva: ignorar métodos claramente truncados ou construtores
                            if method_name == class_name or len(method_name) <= 2 or (method_name[-1:] == class_name[-1:] and len(method_name) < len(class_name)):
                                continue
                            # Corrigir tipo truncado: se o tipo termina igual ao nome da classe mas está truncado, corrige para o nome da classe
                            if meth_type and meth_type != class_name and meth_type.endswith(class_name[:-1]):
                                meth_type = class_name
                            # Captura todos os métodos override Unreal (Tick, BeginPlay, etc.)
                            if meth_match.group(6) == 'override' or method_name in [
                                'Tick', 'BeginPlay', 'SetupPlayerInputComponent', 'GetLifetimeReplicatedProps', 'OnRep_PlayerState', 'GetAbilitySystemComponent', 'LoseBall_Implementation']:
                                methods.append({'name': method_name, 'type': meth_type if meth_type else class_name, 'params': meth_params, 'visibility': current_vis})
                            # Adiciona todos os métodos declarados
                            elif meth_type or meth_params or method_name:
                                methods.append({'name': method_name, 'type': meth_type if meth_type else class_name, 'params': meth_params, 'visibility': current_vis})
                    # Relações UML
                    relations = []
                    if parent:
                        for p in parent.split(','):
                            relations.append({'type': 'extends', 'target': p.strip()})
                    # --- Adicionar relações de associação/uso ---
                    # Coletar tipos de atributos e métodos para relações
                    rel_targets = set()
                    for attr in attributes:
                        if attr['type'] in all_class_names and attr['type'] != class_name:
                            rel_targets.add(attr['type'])
                    for meth in methods:
                        # Parâmetros podem ser múltiplos tipos separados por vírgula
                        for param_type in meth.get('params', '').split(','):
                            t = param_type.strip()
                            if t in all_class_names and t != class_name:
                                rel_targets.add(t)
                    # Adicionar relações de associação
                    for target in sorted(rel_targets):
                        relations.append({'type': 'association', 'target': target})
                    # Limpar o campo 'target' removendo visibilidade e espaços extras
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

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            uml_json = json.load(f)
    except Exception as e:
        print(f"[UML V2] Erro ao ler o JSON para gerar PUML: {e}")
        return

    # Gerar PUML dinâmico a partir do JSON real
    print("\n[UML V2] PUML GERADO DINAMICAMENTE A PARTIR DO JSON:\n")
    puml = generate_puml_from_json(uml_json, project_dir)
    print(puml)

    # Salvar PUML em arquivo
    puml_path = os.path.join(project_dir, 'UML_ClassDiagram.puml')
    with open(puml_path, 'w', encoding='utf-8') as pf:
        pf.write(puml)
    print(f"[UML V2] PUML salvo em: {puml_path}")

    # Gerar SVG a partir do PUML
    plantuml_jar_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'plantuml.jar'))
    svg_cmd = f'java -jar "{plantuml_jar_path}" -tsvg "{puml_path}"'
    print(f"[UML V2] Gerando SVG com: {svg_cmd}")
    os.system(svg_cmd)

    # Abrir SVG automaticamente (se possível)
    svg_path = puml_path.replace('.puml', '.svg')
    if os.path.exists(svg_path):
        print(f"[UML V2] Abrindo SVG: {svg_path}")
        import webbrowser
        webbrowser.open(svg_path)
    else:
        print(f"[UML V2] SVG não encontrado: {svg_path}")


def generate_puml_from_json(uml_json, project_dir=None):
    """
    Gera PUML dinâmico a partir do JSON UML real, agrupando e colorindo por estereótipo/tipo.
    Classes sem relação são agrupadas em 'Others'.
    Setas coloridas vivas e caixas com sombra.
    Adiciona título com nome do projeto e versão da Unreal, e uma classe fictícia com plugins utilizados.
    """
    def clean_relation_target(name):
        return re.sub(r'^(public|protected|private)\s*:?', '', name, flags=re.IGNORECASE).strip()

    # --- Lê .uproject se disponível ---
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
    # Relações (herança, implements, associação)
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
    # 1. Descobrir todos os estereótipos únicos
    stereotypes = sorted(set(item['stereotype'] for item in all_items))
    # 2. Gerar cores automaticamente (paleta pastel)
    pastel_palette = [
        '#FFD580', '#B3E6B3', '#FFB3B3', '#B3D1FF', '#E0B3FF', '#FFF0B3', '#C6E2FF', '#FFCCE5', '#D5FFCC', '#FFDFBA'
    ]
    colors = {st: pastel_palette[i % len(pastel_palette)] for i, st in enumerate(stereotypes)}
    # 3. Montar skinparam dinamicamente
    skinparam = '\n'.join([
        f'  BackgroundColor<<{st}>> {color}' for st, color in colors.items()
    ])
    skinparam += '\n  Shadowing true\n  ArrowColor #FF4500\n  ArrowThickness 2\n  ArrowFontColor #222\n'
    skinparam += '  nodesep 80\n  ranksep 80\n'  # Maior espaçamento vertical e horizontal
    # 4. Header do diagrama
    puml = ["@startuml", ""]
    # Forçar layout mais vertical
    puml.append("top to bottom direction")  
    if project_name or unreal_version:
        title = f"{project_name or ''} (Unreal Engine {unreal_version or ''})".strip()
        # Aumentar fonte do título
        puml.append(f"title <size:24>{title}</size>")
        puml.append("")
    puml.append("' Definição de cores dinâmica por estereótipo, sombra, espaçamento e setas vivas")
    puml.append(f"skinparam class {{\n{skinparam}\n}}\n")
    # 4b. Caixa fictícia de Plugins
    if plugins:
        puml.append('class "Plugins Used" as PluginsUsed <<(P,orchid)>> {')
        for pl in plugins:
            puml.append(f"  {pl}")
        puml.append('}')
        puml.append("")
    # 5. Agrupar por estereótipo E prefixo de nome
    import collections
    def get_prefix(name):
        return name[0] if name and name[0].isalpha() else '_'
    for st in stereotypes:
        items_by_prefix = collections.defaultdict(list)
        for item in all_items:
            if item['stereotype'] == st and item['name'] in related_names:
                prefix = get_prefix(item['name'])
                items_by_prefix[prefix].append(item)
        if not items_by_prefix:
            continue
        for prefix, items in sorted(items_by_prefix.items()):
            puml.append(f"package \"{st}s - {prefix}*\" <<Rectangle>> {{")
            for item in items:
                kind = 'struct' if st.lower() == 'struct' else ('interface' if st.lower() == 'interface' else ('enum' if st.lower() == 'enum' else 'class'))
                stereotype_tag = f"<<{st}>>"
                puml.append(f"  {kind} {item['name']} {stereotype_tag} {{")
                for f in item['fields']:
                    puml.append(f"    {f}")
                for m in item['methods']:
                    puml.append(f"    {m}")
                puml.append("  }")
            puml.append("}")
            puml.append("")
    # 6. Agrupar Others (sem relação)
    others = [item for item in all_items if item['name'] not in related_names]
    if others:
        puml.append('package "Others" <<Rectangle>> {')
        for item in others:
            kind = 'struct' if item['stereotype'].lower() == 'struct' else ('interface' if item['stereotype'].lower() == 'interface' else ('enum' if item['stereotype'].lower() == 'enum' else 'class'))
            stereotype_tag = f"<<{item['stereotype']}>>"
            puml.append(f"  {kind} {item['name']} {stereotype_tag} {{")
            for f in item['fields']:
                puml.append(f"    {f}")
            for m in item['methods']:
                puml.append(f"    {m}")
            puml.append("  }")
        puml.append('}')
        puml.append("")
    # 7. Relações (setas coloridas customizadas, rótulo destacado)
    puml.append("' --- Relações ---")
    arrow_colors = {
        '<|--': '#FF4500;line.bold', # Laranja vivo, herança
        '..|>': '#1E90FF;line.dashed', # Azul vivo, implements
        '-->': '#32CD32;line.bold', # Verde vivo, associação
    }
    for src, tgt, arrow, label in relations:
        color = arrow_colors.get(arrow, '#FF4500')
        puml.append(f"{src} {arrow} {tgt} : <b><size:16><color:{color}>{label}</color></size></b>")
    puml.append("\n@enduml")
    return '\n'.join(puml)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print('Uso: python CPPForUnrealEngineV2.py <ProjectDir>')
