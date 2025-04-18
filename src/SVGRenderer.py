import os
import subprocess
import webbrowser

def render_svg(puml_path):
    """
    Gera um arquivo SVG a partir de um arquivo .puml usando plantuml.jar e abre o SVG no navegador.
    Retorna o caminho do SVG gerado ou None em caso de erro.
    """
    folder = os.path.dirname(os.path.abspath(puml_path))
    svg_file = os.path.splitext(puml_path)[0] + ".svg"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plantuml_jar = os.path.join(script_dir, "plantuml.jar")
    if not os.path.exists(plantuml_jar):
        print(f"[SVGRenderer] plantuml.jar não encontrado em: {plantuml_jar}")
        return None
    if not os.path.exists(puml_path):
        print(f"[SVGRenderer] Arquivo .puml não encontrado: {puml_path}")
        return None
    try:
        subprocess.run([
            "java", "-jar", plantuml_jar, "-tsvg", os.path.basename(puml_path)
        ], cwd=folder, check=True)
        if os.path.exists(svg_file):
            webbrowser.open(svg_file)
            return svg_file
        else:
            print(f"[SVGRenderer] SVG não foi gerado: {svg_file}")
            return None
    except subprocess.CalledProcessError as e:
        print(f"[SVGRenderer] Erro ao gerar SVG: {e}")
        return None
