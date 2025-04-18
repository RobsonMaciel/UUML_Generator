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
    # Adicione mais padrões se quiser
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UML Central App (console)")
    parser.add_argument("--project", "-p", required=True, help="Caminho do projeto (diretório raiz)")
    parser.add_argument("--tipo", "-t", required=True, choices=["cpp4ue", "cpp", "unity", "python"], help="Tipo do projeto: cpp4ue, cpp, unity, python")
    args = parser.parse_args()

    if args.tipo == "cpp4ue":
        from CPPForUnrealEngine import main as gen_cpp4ue
        print(f"[UML] Gerando UML para C++ Unreal em {args.project}")
        try:
            gen_cpp4ue(args.project)
        except Exception as e:
            print(f"[ERRO] Execução interrompida: {e}")
        print("[UML] Finalizado!")
    elif args.tipo == "cpp":
        from CPPGenericUML import generate_puml as gen_cpp
        print(f"[UML] Gerando UML para C++ puro em {args.project}")
        gen_cpp(args.project)
        print("[UML] Finalizado!")
    elif args.tipo == "unity":
        from CSharpForUnity import generate_puml as gen_unity
        print(f"[UML] Gerando UML para Unity C# em {args.project}")
        gen_unity(args.project)
        print("[UML] Finalizado!")
    elif args.tipo == "python":
        from PythonUML import generate_puml as gen_py
        print(f"[UML] Gerando UML para Python em {args.project}")
        gen_py(args.project)
        print("[UML] Finalizado!")
    else:
        print("Tipo de projeto não reconhecido. Use --tipo entre: cpp4ue, cpp, unity, python.")
