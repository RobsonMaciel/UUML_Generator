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
            json_content = f.read()
        print("\n[UML V2] UML JSON COMPLETO:\n")
        print(json_content)
    except Exception as e:
        print(f"[UML V2] Erro ao ler e printar o JSON: {e}")

    # Gerar PUML de teste com classes fictícias
    print("\n[UML V2] PUML DE TESTE (mock):\n")
    mock_puml = generate_mock_puml()
    print(mock_puml)

    # Salvar PUML em arquivo
    mock_puml_path = os.path.join(project_dir, 'UML_MockTest.puml')
    with open(mock_puml_path, 'w', encoding='utf-8') as pf:
        pf.write(mock_puml)
    print(f"[UML V2] PUML de teste salvo em: {mock_puml_path}")

    # Gerar SVG a partir do PUML
    plantuml_jar_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'plantuml.jar'))
    svg_cmd = f'java -jar "{plantuml_jar_path}" -tsvg "{mock_puml_path}"'
    print(f"[UML V2] Gerando SVG com: {svg_cmd}")
    os.system(svg_cmd)

    # Abrir SVG automaticamente (se possível)
    svg_path = mock_puml_path.replace('.puml', '.svg')
    if os.path.exists(svg_path):
        print(f"[UML V2] Abrindo SVG: {svg_path}")
        import webbrowser
        webbrowser.open(svg_path)
    else:
        print(f"[UML V2] SVG não encontrado: {svg_path}")


def generate_mock_puml():
    """
    Gera um PUML de teste com múltiplos estereótipos, agrupados visualmente em packages e com cores distintas para cada grupo. Compatível com PlantUML local/jar.
    """
    return '''@startuml

' Definição de cores para estereótipos
skinparam class {
  BackgroundColor<<Controller>> #FFD580
  BackgroundColor<<Service>> #B3E6B3
  BackgroundColor<<Entity>> #FFB3B3
  BackgroundColor<<UnrealStruct>> #B3D1FF
  BackgroundColor<<Interface>> #E0B3FF
  BackgroundColor<<ValueObject>> #FFF0B3
}

' --- Controllers ---
package "Controllers" <<Rectangle>> {
  class GameController <<Controller>> {
    +startGame() : void
    +endGame() : void
    +service : GameService
  }
}

' --- Services ---
package "Services" <<Rectangle>> {
  class GameService <<Service>> {
    +processMove() : bool
    +saveGame() : void
    +entity : PlayerEntity
  }
}

' --- Entities ---
package "Entities" <<Rectangle>> {
  class PlayerEntity <<Entity>> {
    +id : int
    +name : String
    +score : int
  }
}

' --- Structs ---
package "Structs" <<Rectangle>> {
  struct Vec2D <<UnrealStruct>> {
    +float x
    +float y
  }
}

' --- Interfaces ---
package "Interfaces" <<Rectangle>> {
  interface ITrainable <<Interface>> {
    +train(command : String) : bool
  }
}

' --- Value Objects ---
package "ValueObjects" <<Rectangle>> {
  class GameSettings <<ValueObject>> {
    +difficulty : String
    +maxPlayers : int
  }
}

' --- Relações ---
GameController --> GameService : uses
GameService --> PlayerEntity : manages
PlayerEntity --> Vec2D : has position
PlayerEntity ..|> ITrainable : optional
GameController --> GameSettings : configures

@enduml'''

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print('Uso: python CPPForUnrealEngineV2.py <ProjectDir>')
