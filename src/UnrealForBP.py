import os
import subprocess

# Caminho relativo para o UAssetAPI.dll dentro da pasta UAssetAPI
UASSETAPI_DIR = os.path.join(os.path.dirname(__file__), 'UAssetAPI')
UASSETAPI_CLI_EXE = os.path.join(UASSETAPI_DIR, 'UAssetAPI.CLI.exe')


def find_content_folder(project_root):
    """Procura pela pasta 'Content' dentro do projeto Unreal."""
    for root, dirs, files in os.walk(project_root):
        for d in dirs:
            if d.lower() == 'content':
                return os.path.join(root, d)
    return None


def find_uasset_files(content_folder):
    """Retorna todos os arquivos .uasset dentro da pasta Content (recursivo)."""
    uasset_files = []
    for root, dirs, files in os.walk(content_folder):
        for file in files:
            if file.endswith('.uasset'):
                uasset_files.append(os.path.join(root, file))
    return uasset_files


def export_uasset_to_json(uasset_path, output_json_path, error_log_path=None):
    """Usa o UAssetAPI.CLI.exe self-contained para exportar um .uasset para .json.
    Em caso de erro, registra o arquivo no log de erros."""
    print(f"[LOG] Chamando UAssetAPI.CLI.exe para exportar: {uasset_path}")
    print(f"[LOG] Comando: {UASSETAPI_CLI_EXE} export {uasset_path} {output_json_path}")
    try:
        result = subprocess.run([
            UASSETAPI_CLI_EXE,
            'export',
            uasset_path,
            output_json_path
        ], check=False, capture_output=True, text=True)
        print(f"[LOG] Retorno do processo: {result.returncode}")
        if result.stdout:
            print(f"[STDOUT] {result.stdout}")
        if result.stderr:
            print(f"[STDERR] {result.stderr}")
        if result.returncode != 0:
            print(f"[ERRO] Falha ao exportar {uasset_path}: {result.stderr}")
            if error_log_path:
                with open(error_log_path, 'a', encoding='utf-8') as elog:
                    elog.write(f"{uasset_path}\n")
    except Exception as e:
        print(f"[EXCEPTION] Falha ao executar UAssetAPI.CLI.exe: {e}")
        if error_log_path:
            with open(error_log_path, 'a', encoding='utf-8') as elog:
                elog.write(f"{uasset_path}\n")


def batch_export_blueprints_to_json(project_root, output_dir=None):
    print(f"[LOG] Iniciando batch_export_blueprints_to_json para: {project_root}")
    content_folder = find_content_folder(project_root)
    print(f"[LOG] Pasta Content detectada: {content_folder}")
    if not content_folder:
        print("[ERRO] Pasta 'Content' não encontrada no projeto Unreal!")
        return
    # Define output_dir como ./UAssetToJson se não for passado
    if output_dir is None:
        output_dir = os.path.abspath(os.path.join(os.getcwd(), 'UAssetToJson'))
    print(f"[LOG] Pasta de saída dos JSONs: {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    error_log_path = os.path.join(output_dir, 'log-error.txt')
    # Limpa o log de erro anterior
    open(error_log_path, 'w').close()
    uasset_files = find_uasset_files(content_folder)
    print(f"[LOG] {len(uasset_files)} arquivos .uasset encontrados.")
    for uasset in uasset_files:
        # Caminho relativo do .uasset em relação à pasta Content
        rel_path = os.path.relpath(uasset, project_root)
        # Troca extensão para .json
        json_rel_path = os.path.splitext(rel_path)[0] + '.json'
        # Caminho de saída espelhando a estrutura
        output_json = os.path.join(output_dir, json_rel_path)
        # Cria diretório espelhado se necessário
        output_json_dir = os.path.dirname(output_json)
        if not os.path.exists(output_json_dir):
            os.makedirs(output_json_dir)
        print(f"[LOG] Extraindo {uasset} -> {output_json}")
        export_uasset_to_json(uasset, output_json, error_log_path=error_log_path)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Uso: python UnrealForBP.py <UnrealProjectRoot> [<OutputJsonDir>]")
        exit(1)
    project_root = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    batch_export_blueprints_to_json(project_root, output_dir)
