# 🦩 Uuml – UML Generator for Unreal Engine

## 📘 English Version

**Uuml** is a cross-platform visual application written in Python with a modern `customtkinter` GUI, designed to automatically generate UML diagrams from Unreal Engine C++ source code.

## 🔧 Features

- Unified single-file Python codebase for easy maintenance and build
- Elegant graphical interface with log preview and real-time feedback
- Automatically detects the `CodeExamples` folder (containing Unreal Engine C++ header examples)
- Extracts:
  - **Classes** (`UCLASS`)
  - **Methods** (`UFUNCTION`)
  - **Attributes** (`UPROPERTY`)
- Detects Unreal project name and engine version from `.uproject`
- Generates `.puml` grouped by class type:
  - `GameModes`, `Characters`, `Controllers`, `Components`, `Actors`, etc.
- Identifies and draws class dependencies based on used attributes
- Cleans up irrelevant lines (e.g., getters, `const override`, macro-only lines)
- Applies a unique **color per package** for better visual separation
- Generates final **SVG diagram** and opens it in the browser

## 🌈 Visual Style (PlantUML)

- Dark theme (`#1e1e1e`) with white fonts and vivid package borders
- Direction: `left to right`
- Layout: `smetana` (optimal positioning)
- Each package has its own color:
  - `Actors`: blue
  - `Characters`: orange
  - `Controllers`: teal
  - `GameModes`: purple
  - `Components`: cyan
  - `HUD`: green
  - etc...
- Smooth arrows, spacing, and organized layout

## 🚀 How to Use

1. Make sure you have **Java 17+** installed.
2. Go to the `src` folder. All code, the executable, icon, and `plantuml.jar` are there.
3. Run `UnrealUML_APP.py` (or the compiled `.exe`).
4. The app will:
   - Detect your `CodeExamples` folder (with Unreal C++ headers for testing)
   - Generate `.puml` based on Unreal C++ headers
   - Clean the `.puml` file
   - Render `.svg` with PlantUML
   - Open the final SVG automatically

## ⚙️ Requirements

- **Python 3.9+** (if using scripts)
- **Java 17+**
- Python packages:
  - `customtkinter`
  - `tkinter`

> If Java is missing or outdated, the tool will guide you to install JDK 17.0.12.

## 📁 Project Structure

```
/UnrealUML
  /src
    UnrealUML_APP.py
    UnrealUML_APP.exe
    unrealuml_icon.ico
    plantuml.jar
  /CodeExamples
    (all .h files for testing)
  README.md, LICENSE, etc.
```

## 📥 How to Get `plantuml.jar`

You can download the latest version of PlantUML from:
https://plantuml.com/download

Place the `plantuml.jar` file inside the `src` folder.

## 📝 Notes

- All Python and executable files are now inside the `src` directory for better organization.
- Example Unreal Engine C++ headers for testing are in `CodeExamples`.
- The project is ready for packaging and distribution as a single .exe with a custom icon.

---

## 📗 Versão em Português

**Uuml** é uma aplicação visual moderna feita em Python com `customtkinter`, que gera automaticamente diagramas UML a partir de projetos Unreal Engine em C++.

## 🔧 Funcionalidades

- Interface com botão "Gerar Tudo" e área de log ao vivo.
- Detecção automática da pasta `CodeExamples`.
- Extração de:
  - **Classes** (`UCLASS`)
  - **Métodos** (`UFUNCTION`)
  - **Atributos** (`UPROPERTY`)
- Leitura do nome do projeto e versão do `.uproject`.
- Agrupamento de classes em pacotes lógicos com **cores distintas**.
- Identificação de dependências entre classes com base nos atributos.
- Remoção automática de linhas irrelevantes (e.g., `const`, `ATTRIBUTE_ACCESSORS`, getters/setters).
- Geração de `SeuProjeto.puml` → limpeza → `SeuProjeto.svg`.
- Visualização automática do diagrama no navegador.

## 🌈 Estilo Visual

- Tema escuro com layout `left to right`, algoritmo `smetana`.
- Cores por pacote:
  - `Actors`: azul
  - `Characters`: laranja
  - `Controllers`: ciano escuro
  - `GameModes`: roxo
  - `Components`: azul claro
  - `HUD`: verde
  - etc...
- Bordas em destaque, fontes claras, setas suaves e espaçamento ideal.

## 🚀 Como Usar

1. Instale o Java 17+.
2. Vá para a pasta `src`. Todos os arquivos de código, executável, ícone e `plantuml.jar` estão lá.
3. Execute `UnrealUML_APP.py` (ou o compilado `.exe`).
4. O app irá:
   - Detectar a pasta `CodeExamples` (com headers C++ do Unreal Engine para teste)
   - Gerar `.puml` com base nos headers C++ do Unreal Engine
   - Limpar o arquivo `.puml`
   - Renderizar `.svg` com PlantUML
   - Abrir o diagrama final no navegador automaticamente

## 📦 Empacotamento

```bash
python -m PyInstaller --onefile --noconsole --icon=unrealuml_icon.ico UnrealUML_APP.py
```

## 👤 Autor

Desenvolvido por **Robson Franco Maciel** para profissionais de Unreal Engine que precisam visualizar, documentar e entender a arquitetura de grandes projetos de forma clara.

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

## 🖼️ Logo

![Uuml Logo](images/logo.png)

---

**Uuml** nasceu para facilitar a leitura estrutural de grandes projetos Unreal. Ideal para documentação, times distribuídos, onboarding técnico e engenharia reversa visual.
