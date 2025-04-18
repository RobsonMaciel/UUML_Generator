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

def detect_project_type(project_dir):
    # Unreal Engine: pasta Source com .h/.cpp
    source_dir = os.path.join(project_dir, 'Source')
    if os.path.isdir(source_dir):
        for root, _, files in os.walk(source_dir):
            if any(f.endswith('.h') or f.endswith('.cpp') for f in files):
                return 'cpp4ue'
    # Unity: arquivos .cs e possíveis arquivos de projeto Unity
    if any(f.endswith('.cs') for f in os.listdir(project_dir)):
        return 'unity'
    # Python: arquivos .py
    if any(f.endswith('.py') for f in os.listdir(project_dir)):
        return 'python'
    # Puro C++
    if any(f.endswith('.cpp') or f.endswith('.h') for f in os.listdir(project_dir)):
        return 'cpp'
    return None

def get_project_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
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
            input('Press any key to exit...')
        sys.exit(1)

    if tipo == "cpp4ue":
        from CPPForUnrealEngine import main as gen_cpp4ue
        print(f"[UML] Generating UML for C++ Unreal in {project_dir}")
        try:
            gen_cpp4ue(project_dir)
        except Exception as e:
            print(f"[ERROR] Execution interrupted: {e}")
        print("[UML] Finished!")
    elif tipo == "cpp":
        from CPPGenericUML import generate_puml as gen_cpp
        print(f"[UML] Generating UML for pure C++ in {project_dir}")
        gen_cpp(project_dir)
        print("[UML] Finished!")
    elif tipo == "unity":
        from CSharpForUnity import generate_puml as gen_unity
        print(f"[UML] Generating UML for Unity C# in {project_dir}")
        gen_unity(project_dir)
        print("[UML] Finished!")
    elif tipo == "python":
        from PythonUML import generate_puml as gen_py
        print(f"[UML] Generating UML for Python in {project_dir}")
        gen_py(project_dir)
        print("[UML] Finished!")
    else:
        print("Unrecognized project type. Use --type among: cpp4ue, cpp, unity, python.")
        if getattr(sys, 'frozen', False):
            input('Press any key to exit...')
        sys.exit(1)
