# 🦩 Uuml – Universal UML Diagram Generator

## Overview

**Uuml** is a cross-platform, modern visual application to automatically generate beautiful UML class diagrams from source code in multiple languages. With a single interface, you can visualize, document, and understand the architecture of any large project — Unreal Engine, Unity, C++, C#, Python, and more!

---

## ✨ Key Features

- **Multi-language support:**
  - C++ (generic)
  - C++ for Unreal Engine (UCLASS/UFUNCTION/UPROPERTY detection)
  - C# (generic)
  - C# for Unity (MonoBehaviour, ScriptableObject, custom grouping)
  - Python
  - Java (planned)
  - Easily extensible for more!
- **Automatic class, method, and property extraction** for all supported languages
- **Smart grouping:** Classes grouped by package, stereotype, or logical module, with vivid color coding
- **Modern dark visual style:** White text, colored borders, clear arrows, optimal layout
- **No duplicate classes, no naming conflicts:** Robust PlantUML output
- **Real-time logging:** Progress and errors are shown in the interface
- **One-click export:** Generates `.puml` and `.svg` files, opens the diagram automatically
- **Modular pipeline:** Easy to add new languages or customize extraction logic
- **Cross-platform:** Works on Windows, Mac, and Linux

---

## 🌍 Supported Languages & Features

| Language               | Grouping/Color | Methods & Props | Special Features                      |
|-----------------------|:--------------:|:---------------:|---------------------------------------|
| C++                   |      ✔️        |       ✔️        |                                       |
| C++ for Unreal Engine |      ✔️        |       ✔️        | UCLASS/UFUNCTION/UPROPERTY detection  |
| C#                    |      ✔️        |       ✔️        |                                       |
| C# for Unity          |      ✔️        |       ✔️        | MonoBehaviour/ScriptableObject groups |
| Python                |                |                 |                                       |
| Java                  |                |                 |                                       |
| Blueprint for Unreal Engine |           |                 |                                       |

---

## 🎨 Visual Style

- Dark background, white fonts, vivid package/class colors
- Smooth arrows, optimal spacing, and clear grouping
- All text inside class boxes is white for maximum contrast

---

## 🚀 How to Use

1. Install **Java 17+** (required for PlantUML rendering)
2. Download or clone this repository
3. Go to the `src` folder
4. Run `UumlCentralApp.py` (or the compiled `.exe`)
5. Select your project root and target language
6. Click "Generate" — your UML diagram appears in seconds!

---

## 🏗️ Project Structure

```
/Uuml
  /src
    UumlCentralApp.py
    CSharpForUnity.py
    CPPForUnrealEngine.py
    # ...other language modules
    plantuml.jar
    unrealuml_icon.ico
  /CodeExamples
  README.md, LICENSE, etc.
```

---

## ⚙️ Requirements

- **Python 3.9+** (if using scripts)
- **Java 17+**
- Python packages:
  - `customtkinter`
  - `tkinter`

> If Java is missing or outdated, the tool will guide you to install JDK 17.0.12.

---

## 🛠️ Building a Standalone Executable

To create a standalone executable (Windows example):

```
pip install pyinstaller
cd src
pyinstaller --onefile --noconsole --icon=unrealuml_icon.ico UumlCentralApp.py
```
- The executable will be in `dist/UumlCentralApp.exe`.
- You must include `plantuml.jar` in the same folder as the executable.

---

## 📝 Notes

- All scripts and executables are inside `src` for easy organization.
- Language selection is automatic or manual.
- Example code for testing is in `CodeExamples`.
- The project is ready for packaging and distribution as a single .exe with a custom icon.

---

## 👤 Author & Credits

Developed by **Robson Franco Maciel** and contributors.

- **PlantUML**: Diagram rendering powered by [PlantUML](https://plantuml.com/). PlantUML is © Arnaud Roques, used under the [PlantUML License](https://plantuml.com/license).
- **CustomTkinter**: Modern Python GUI library by Tom Schimansky.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🖼️ Logo

![Uuml Logo](images/logo.png)

---

**Uuml** is ideal for documentation, onboarding, distributed teams, and visual reverse engineering — for any codebase!
