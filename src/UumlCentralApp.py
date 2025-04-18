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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UML Central App (console)")
    parser.add_argument("--project", "-p", required=True, help="Project path (root directory)")
    parser.add_argument("--type", "-t", required=True, choices=["cpp4ue", "cpp", "unity", "python"], help="Project type: cpp4ue, cpp, unity, python")
    args = parser.parse_args()

    if args.type == "cpp4ue":
        from CPPForUnrealEngine import main as gen_cpp4ue
        print(f"[UML] Generating UML for C++ Unreal in {args.project}")
        try:
            gen_cpp4ue(args.project)
        except Exception as e:
            print(f"[ERROR] Execution interrupted: {e}")
        print("[UML] Finished!")
    elif args.type == "cpp":
        from CPPGenericUML import generate_puml as gen_cpp
        print(f"[UML] Generating UML for pure C++ in {args.project}")
        gen_cpp(args.project)
        print("[UML] Finished!")
    elif args.type == "unity":
        from CSharpForUnity import generate_puml as gen_unity
        print(f"[UML] Generating UML for Unity C# in {args.project}")
        gen_unity(args.project)
        print("[UML] Finished!")
    elif args.type == "python":
        from PythonUML import generate_puml as gen_py
        print(f"[UML] Generating UML for Python in {args.project}")
        gen_py(args.project)
        print("[UML] Finished!")
    else:
        print("Unrecognized project type. Use --type among: cpp4ue, cpp, unity, python.")
