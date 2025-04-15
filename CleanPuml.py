import os
import re

def clean_puml(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    cleaned_lines = []
    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue
        if stripped.startswith("class ") and re.match(r"class\s+\w+$", stripped):
            continue
        if stripped in ["const", "const override"]:
            continue
        if "ATTRIBUTE_ACCESSORS" in stripped:
            continue
        if stripped.startswith("return "):
            continue

        cleaned_lines.append(line)

    with open(output_path, "w", encoding="utf-8") as file:
        file.writelines(cleaned_lines)

    os.replace(output_path, input_path)
    return input_path

if __name__ == "__main__":
    current_dir = os.getcwd()
    puml_file = next((f for f in os.listdir(current_dir) if f.endswith(".puml")), None)

    if not puml_file:
        print("Nenhum arquivo .puml encontrado para limpar.")
        exit(1)

    original_path = os.path.join(current_dir, puml_file)
    cleaned_path = original_path.replace(".puml", "_cleaned.puml")

    final_path = clean_puml(original_path, cleaned_path)
    print(f"PUML limpo salvo como: {final_path}")
