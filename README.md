# Uuml – Universal UML Diagram Generator

## Overview

Uuml is a cross-platform visual application for automatically generating UML diagrams from C++, C# (Unity and pure), Python, Go, Unreal Engine, and more. Ideal for visualizing, documenting, and quickly understanding the architecture of any project.

---

## Key Features

- Support for multiple languages: C++, C++ Unreal Engine, C#, C# Unity, C# puro, Python, Go, Java (coming soon)
- Automatic extraction of classes, methods, attributes, structs, enums, and interfaces
- Intelligent grouping by package, stereotype, or module, with vivid colors
- Modern (dark) visual style, white or black text (depending on theme), colored borders, clear arrows, and optimized layout
- No duplicate classes or naming conflicts
- Real-time progress and error logging
- One-click export to `.puml` and `.svg`
- Modular and easy to extend for new languages
- Works on Windows, Mac, and Linux

---

## Supported Languages & Features

| Language                     | Grouping/Color | Methods & Props | Special Features                                | Planned/Future |
|------------------------------|:--------------:|:---------------:|------------------------------------------------|:--------------:|
| C++                          |      ✔️        |       ✔️        | Standard C++ support, class/struct/enum parsing |                |
| C++ for Unreal Engine        |      ✔️        |       ✔️        | UCLASS/UFUNCTION/UPROPERTY detection           |                |
| C# (puro)                    |      ✔️        |       ✔️        | Pure C# support, full class/interface parsing   |                |
| C# for Unity                 |      ✔️        |       ✔️        | MonoBehaviour/ScriptableObject groups          |                |
| Python                       |      ✔️        |       ✔️        | Grouped by module, colored packages, <<PythonClass>> stereotype |                |
| Go                           |      ✔️        |       ✔️        | Structs, interfaces, methods, package grouping  |                |
| Java                         |                |                 |                                                |       ✔️       |
| Blueprint for Unreal Engine  |                |                 |                                                |       ✔️       |

---

## Visual Style

- The generated UML diagrams use PlantUML's rendering engine, with custom colors and grouping applied via `skinparam`.
- Classes and packages may be grouped and colored by stereotype, module, or language (e.g., <<PythonClass>>, <<CppModule>>, <<MonoBehaviour>>).
- Modern dark background, black text inside boxes, neon/glow arrows for high contrast.
- The final look of the diagrams may vary depending on PlantUML version and user settings.

---

## How to Use

1. Install **Java 17+** (required to render PlantUML)
2. Install **Python 3.9+**
3. Install the Python package: `tkinter`
4. Download or clone this repository
5. Go to the `src` folder
6. Run `UumlCentralApp.py` (or the `.exe` executable)
7. Select the project directory and target language
8. Click "Generate" to create the UML diagram

### Command Line

It is also possible to generate diagrams via terminal:

```bash
python src/UumlCentralApp.py --project path/to/UnrealProject --type cpp4ue
python src/UumlCentralApp.py --project path/to/UnityProject --type unity
python src/UumlCentralApp.py --project path/to/CSharpProject --type csharp
python src/UumlCentralApp.py --project path/to/GoProject --type go
python src/UumlCentralApp.py --project path/to/PythonProject --type python
```

- The `.puml` file will be generated at the root of the project.
- If Java and PlantUML are available, the `.svg` will be generated and opened automatically.
- For Unreal Engine, an `entities.txt` is also created with all detected entities.

---

## Project Structure

```
/Uuml
  /src
    UumlCentralApp.py
    CSharpUML.py
    CSharpForUnity.py
    CPPForUnrealEngine.py
    CPPGenericUML.py
    GoUML.py
    SVGRenderer.py
    /UAssetAPI
      UAssetAPI.dll
      UAssetAPI.pdb
      UAssetAPI.deps.json
      UAssetAPI.runtimeconfig.json
      # ...other UAssetAPI dependencies (e.g., Newtonsoft.Json.dll)
    plantuml.jar
    unrealuml_icon.ico
    # ...other modules
  /CodeExamples
  README.md, LICENSE, etc.
```

---

## Requirements

- **Python 3.9+**
- **Java 17+**
- Python package: `tkinter`

> If Java is missing/outdated, the app will guide you to install JDK 17.

---

## Standalone Executable

To create a standalone executable (Windows) with all Python modules embedded, follow these steps:

- Todos os arquivos da pasta `published-cli` devem ser copiados para `src/UAssetAPI`.
- O comando PyInstaller deve incluir todos os arquivos da subpasta UAssetAPI:

```powershell
python -m PyInstaller --onefile --icon=UumlCentralApp.ico \
  --add-data "plantuml.jar;." \
  --add-data "UAssetAPI/*;UAssetAPI" \
  --hidden-import=CPPForUnrealEngine \
  --hidden-import=CSharpForUnity \
  --hidden-import=CPPGenericUML \
  --hidden-import=CSharpUML \
  --hidden-import=GoUML \
  UumlCentralApp.py
```

- Isso garante que todas as dependências do .NET e do UAssetAPI estejam disponíveis no pacote final.

- Coloque todos os arquivos do UAssetAPI (DLL, .json, .pdb, etc) na subpasta `src/UAssetAPI`.
- Se houver outros arquivos/dlls necessários, adicione-os na mesma linha.
- The executable will be created in `src/dist/UumlCentralApp.exe`.
- Place `plantuml.jar` in the same folder as the executable for PlantUML export.
- Run the executable from the command line or use the provided `.bat` script to pass parameters.

---

## Current Features

- Support for C++, C++ Unreal Engine, C# (Unity and puro), Python, Go
- Automatic generation of classes, methods, attributes, structs, enums, and interfaces
- Intelligent visual grouping by package, stereotype, or module
- Modern visual style, diagrams ready for documentation
- Easy export to PlantUML and SVG
- Modular and ready for new languages

---

## Roadmap / Upcoming Features

- Full support for Java
- Enhanced support for Unreal Engine Blueprints
- More visual customization options
- Support for other UML diagram types

---

## Author & Credits

Developed by **Robson Franco Maciel** and contributors.

- **PlantUML**: Diagrams by [PlantUML](https://plantuml.com/)

---

## 🖼️ Logo

![Uuml Logo](images/logo.png)

---

## License

This project is licensed under the [MIT License](LICENSE).

---

Uuml is ideal for documentation, onboarding, distributed teams, and visual reverse engineering of any code!
