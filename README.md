# Uuml – Universal UML Diagram Generator

## Overview

Uuml is a cross-platform visual application for automatically generating UML diagrams from C++, C# (Unity), Python, Unreal Engine, and other projects. Ideal for visualizing, documenting, and quickly understanding the architecture of any project.

---

## Key Features

- Support for multiple languages: C++, C++ Unreal Engine, C#, C# Unity, Python, Java (coming soon)
- Automatic extraction of classes, methods, attributes, structs, enums, and interfaces
- Intelligent grouping by package, stereotype, or module, with vivid colors
- Modern (dark) visual style, white text, colored borders, clear arrows, and optimized layout
- No duplicate classes or naming conflicts
- Real-time progress and error logging
- One-click export to `.puml` and `.svg`
- Modular and easy to extend for new languages
- Works on Windows, Mac, and Linux

---

## Supported Languages & Features

| Language                     | Grouping/Color | Methods & Props | Special Features                                | Planned/Future |
|------------------------------|:--------------:|:---------------:|------------------------------------------------|:--------------:|
| C++                          |                |                 |                                                |       ✔️       |
| C++ for Unreal Engine        |      ✔️        |       ✔️        | UCLASS/UFUNCTION/UPROPERTY detection           |                |
| C#                           |                |                 |                                                |       ✔️       |
| C# for Unity                 |      ✔️        |       ✔️        | MonoBehaviour/ScriptableObject groups          |                |
| Python                       |      ✔️        |       ✔️        | Grouped by module, colored packages, <<PythonClass>> stereotype |                |
| Java                         |                |                 |                                                |       ✔️       |
| Blueprint for Unreal Engine  |                |                 |                                                |       ✔️       |

---

## Visual Style

- The generated UML diagrams use PlantUML's rendering engine, with some custom colors and grouping applied via `skinparam`.
- Classes and packages may be grouped and colored by stereotype, module, or language (e.g., <<PythonClass>>, <<CppModule>>, <<MonoBehaviour>>).
- Some elements may have custom borders or background colors, but the overall appearance depends on PlantUML's theme and rendering.
- There is no in-app "dark mode" UI; the "modern" look refers to the diagram output as styled by PlantUML.
- Not all languages or elements use vivid colors; grouping and coloring are primarily for classes by stereotype or module.
- The final look of the diagrams may vary depending on PlantUML version and user settings.

---

## How to Use

1. Install **Java 17+** (required to render PlantUML)
2. Install **Python 3.9+** (if using scripts)
3. Install the Python package:
   - `tkinter`
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
    CSharpForUnity.py
    CPPForUnrealEngine.py
    # ...other modules
    plantuml.jar
    unrealuml_icon.ico
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

To create a standalone executable (Windows) with all Python modules embedded, run the following command from the `src` directory:

```powershell
python -m PyInstaller --onefile --add-data "plantuml.jar;." --hidden-import=CPPForUnrealEngine --hidden-import=CSharpForUnity --hidden-import=CPPGenericUML UumlCentralApp.py
```
- The executable will be created in `src/dist/UumlCentralApp.exe`.
- Place `plantuml.jar` in the same folder as the executable for PlantUML export.
- Run the executable from the command line or use the provided `.bat` script to pass parameters.

---

## Current Features

- Support for C++, C++ Unreal Engine, C# (Unity), Python
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
