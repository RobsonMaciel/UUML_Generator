import os
import subprocess
import webbrowser

def find_puml_file():
    for file in os.listdir():
        if file.endswith(".puml"):
            return os.path.abspath(file)
    return None

def render_svg(puml_path):
    folder = os.path.dirname(puml_path)
    base_name = os.path.splitext(os.path.basename(puml_path))[0]
    svg_file = os.path.join(folder, f"{base_name}.svg")

    try:
        subprocess.run(["java", "-jar", "plantuml.jar", "-tsvg", os.path.basename(puml_path)], cwd=folder, check=True)
        if os.path.exists(svg_file):
            print(f"SVG gerado com sucesso: {svg_file}")
            webbrowser.open(svg_file)
        else:
            print("Erro: SVG não foi gerado.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar PlantUML: {e}")

if __name__ == "__main__":
    puml_file = find_puml_file()
    if puml_file:
        render_svg(puml_file)
    else:
        print("Nenhum arquivo .puml encontrado na pasta atual.")
