import argparse
import os
import sys

LANGUAGES = [
    ("C#", [".cs"]),
    ("Java", [".java"]),
    ("C++", [".cpp", ".h", ".hpp", ".cc", ".cxx"]),
    ("C++ for Unreal", [".h", ".cpp"]),
    ("C# for Unity", [".cs"]),
    ("Python", [".py"]),
]

PROJECT_SIGNATURES = {
    "C# for Unity": ["UnityEngine", "MonoBehaviour"],
    "C++ for Unreal": ["UCLASS", ".uproject"],
}

def find_files_with_ext(root, exts, exclude_dirs=None):
    for dirpath, dirnames, filenames in os.walk(root):
        if exclude_dirs and any(ex in dirpath for ex in exclude_dirs):
            continue
        for f in filenames:
            if any(f.endswith(ext) for ext in exts):
                print(f"DEBUG: found {f} in {dirpath}")
                return True
    print(f"DEBUG: no files with extensions {exts} found in {root}")
    return False

def detect_project_type(project_dir):
    # Unreal Engine: .uproject obrigatório + Source com .h/.cpp
    uproject_files = [f for f in os.listdir(project_dir) if f.endswith('.uproject')]
    source_dir = os.path.join(project_dir, 'Source')
    if uproject_files and os.path.isdir(source_dir) and find_files_with_ext(source_dir, ['.h', '.cpp']):
        return 'cpp4ue'
    # Unity
    if find_files_with_ext(project_dir, ['.cs']) and (
        os.path.exists(os.path.join(project_dir, 'Assembly-CSharp.csproj')) or
        os.path.isdir(os.path.join(project_dir, 'ProjectSettings'))
    ):
        return 'unity'
    # Python
    if find_files_with_ext(project_dir, ['.py']):
        return 'python'
    # C++ puro (mas não Unreal)
    if find_files_with_ext(project_dir, ['.cpp', '.h'], exclude_dirs=['Source']):
        return 'cpp'
    return None

def get_project_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    import sys
    try:
        parser = argparse.ArgumentParser(description="UML Central App (console)")
        parser.add_argument("--project", "-p", required=False, help="Project path (root directory)")
        parser.add_argument("--type", "-t", required=False, choices=["cpp4ue", "cpp", "unity", "python"], help="Project type: cpp4ue, cpp, unity, python")
        args = parser.parse_args()

        # Definir diretório do projeto
        project_dir = args.project if args.project else get_project_dir()
        # Definir tipo do projeto
        tipo = args.type if args.type else detect_project_type(project_dir)
        if not tipo:
            print("[UML] ERROR: Could not detect project type automatically. Please specify --type.")
            print("[UML] Supported types: cpp4ue, cpp, unity, python.")
            if getattr(sys, 'frozen', False):
                input('Pressione ENTER para sair...')
            sys.exit(1)

        if tipo == "cpp4ue":
            from CPPForUnrealEngine import main as gen_cpp4ue
            print(f"[UML] Generating UML for C++ Unreal in {project_dir}")
            try:
                gen_cpp4ue(project_dir)
            except Exception as e:
                print(f"[ERROR] Execution interrupted: {e}")
            print("[UML] Finished!")
            if getattr(sys, 'frozen', False):
                input('Pressione ENTER para sair...')
        elif tipo == "cpp":
            from CPPGenericUML import main as gen_cpp
            from CSharpForUnity import render_svg
            print(f"[UML] Generating UML for pure C++ in {project_dir}")
            gen_cpp(project_dir)
            print("[UML] Finished!")
            if getattr(sys, 'frozen', False):
                input('Pressione ENTER para sair...')
        elif tipo == "unity":
            from CSharpForUnity import generate_puml as gen_unity, render_svg
            print(f"[UML] Generating UML for Unity C# in {project_dir}")
            puml_path = gen_unity(project_dir)
            svg = render_svg(puml_path)
            if svg:
                print(f"[UML] SVG generated: {svg}")
            else:
                print("[UML] SVG not generated!")
            print("[UML] Finished!")
            if getattr(sys, 'frozen', False):
                input('Pressione ENTER para sair...')
        elif tipo == "python":
            from PythonUML import generate_puml as gen_py
            from CSharpForUnity import render_svg
            print(f"[UML] Generating UML for Python in {project_dir}")
            puml_path = gen_py(project_dir)
            svg = render_svg(puml_path)
            if svg:
                print(f"[UML] SVG generated: {svg}")
            else:
                print("[UML] SVG not generated!")
            print("[UML] Finished!")
            if getattr(sys, 'frozen', False):
                input('Pressione ENTER para sair...')
        else:
            print("Unrecognized project type. Use --type among: cpp4ue, cpp, unity, python.")
            if getattr(sys, 'frozen', False):
                input('Pressione ENTER para sair...')
            sys.exit(1)
    except Exception as e:
        import traceback
        print('--- ERRO DE EXECUÇÃO ---')
        print(e)
        traceback.print_exc()
    input('\nPressione ENTER para sair...')
