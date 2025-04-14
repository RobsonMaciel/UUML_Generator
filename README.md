# UnrealUML Generator

**UnrealUML Generator** is a cross-platform visual application written in Python with a `customtkinter` interface, designed to automatically generate UML diagrams from the source code of an Unreal Engine project.

---

**UnrealUML Generator** é uma aplicação visual multiplataforma feita em Python com interface `customtkinter`, projetada para gerar diagramas UML automaticamente a partir do código-fonte de um projeto Unreal Engine.

## 🔧 Features | Funcionalidades

- Visual interface to select the project's `Source` folder.
- Automatically detects the `Source` folder on startup.
- Automatically extracts:
  - Classes (`UCLASS` based)
  - Methods (`UFUNCTION` based)
  - Attributes (`UPROPERTY` based)
- Identifies project name and Unreal version (.uproject).
- Generates a `.puml` file organized into packages by class type:
  - `GameModes`, `Characters`, `Controllers`, `Components`, etc.
- Creates dependency relationships between classes that use attributes of another class type.
- Renders final UML image in **SVG** format with a dark theme.
- Automatically opens the SVG in the default browser after generation.

## 🌟 Visual Style (PlantUML) | Estilo Visual (PlantUML)

- Dark background (`#1e1e1e`), white fonts for contrast.
- Light blue color palette for borders and arrows (`#00bfff`).
- Classes grouped into logical packages (HUD, Actors, Controllers, etc).
- Consistent fonts for classes, methods, and attributes.
- Vertical layout with orthogonal lines (`top to bottom`, `linetype ortho`).

## 🚀 How to Use | Como usar

1. Run `UnrealUML_Generator.exe` (or run the Python script directly if preferred).
2. The `Source` folder will be auto-detected. If needed, change it manually.
3. Click **"Generate Diagram"**.
4. The app will generate `YourProject.puml` and convert it into `YourProject.svg`.
5. The SVG will open automatically in your default browser.

> ⚠️ Requires `plantuml.jar` in the same folder as the executable/script to generate the image.

## 🛠 Requirements | Requisitos

- Python 3.9+ (if using script version)
- Java installed (to run `plantuml.jar`)
- Python libraries:
  - `customtkinter`
  - `tkinter`

## 🔍 Output Example | Exemplo de Saída

- `SuperKidStreetSoccer.puml`
- `SuperKidStreetSoccer.svg`
- Automatically opens the image with classes grouped by package

## 🧑‍💻 Author | Autor

Developed by [Robson Franco Maciel] focused on Unreal Engine projects.

Desenvolvido por [Robson Franco Maciel] com foco em projetos Unreal Engine.

---

## 📦 Packaging with PyInstaller | Empacotamento com PyInstaller

To package the app as a `.exe`, use the following generic command:

Para empacotar o app em `.exe`, use o seguinte comando genérico:

```bash
pyinstaller --onefile --noconsole --icon=unrealuml_icon.ico UnrealUML_Generator.py
```

To force a full rebuild (clean cache):

Para forçar a recompilação total (limpeza de cache):

```bash
pyinstaller --onefile --noconsole --clean --icon=unrealuml_icon.ico UnrealUML_Generator.py
```

> Make sure you are in the same folder as the script and that `plantuml.jar` is available.

> Certifique-se de estar no mesmo diretório do script e com `plantuml.jar` disponível.

---
**UnrealUML Generator** is a tool that makes it easy to understand the architecture of Unreal Engine projects. Ideal for documentation, team onboarding, and fast structure visualization.

**UnrealUML Generator** é uma ferramenta que facilita a compreensão estrutural de projetos Unreal Engine. Ideal para documentação, onboarding de equipes e visualização rápida da arquitetura geral do jogo.

