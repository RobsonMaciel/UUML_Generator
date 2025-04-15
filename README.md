# 🦩 Uuml – UML Generator for Unreal Engine

## 📘 English Version

**Uuml** is a cross-platform visual application written in Python with a modern `customtkinter` GUI, designed to automatically generate UML diagrams from Unreal Engine C++ source code.

## 🔧 Features

- Elegant graphical interface with log preview and real-time feedback.
- Automatically detects the `Source` folder.
- Extracts:
  - **Classes** (`UCLASS`)
  - **Methods** (`UFUNCTION`)
  - **Attributes** (`UPROPERTY`)
- Detects Unreal project name and engine version from `.uproject`.
- Generates `.puml` grouped by class type:
  - `GameModes`, `Characters`, `Controllers`, `Components`, `Actors`, etc.
- Identifies and draws class dependencies based on used attributes.
- Cleans up irrelevant lines (e.g., getters, `const override`, macro-only lines).
- Applies a unique **color per package** for better visual separation.
- Generates final **SVG diagram** and opens it in the browser.

## 🌈 Visual Style (PlantUML)

- Dark theme (`#1e1e1e`) with white fonts and vivid package borders.
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
- Smooth arrows, spacing, and organized layout.

## 🚀 How to Use

1. Make sure you have **Java 17+** installed.
2. Download `plantuml.jar` and place it in the project folder.
3. Run `run_all.py` (or the compiled `.exe`).
4. The app will:
   - Detect your `Source` folder.
   - Generate `.puml` based on Unreal C++ headers.
   - Clean the `.puml` file.
   - Render `.svg` with PlantUML.
   - Open the final SVG automatically.

## ⚙️ Requirements

- **Python 3.9+** (if using scripts)
- **Java 17+**
- Python packages:
  - `customtkinter`
  - `tkinter`

> If Java is missing or outdated, the tool will guide you to install JDK 17.0.12.

## 📅 Get `plantuml.jar`

- Official download: [https://plantuml.com/download](https://plantuml.com/download)
- Place `plantuml.jar` in the **same folder** as the scripts or executable.

## 🔍 Output Example

- `YourProjectName.puml`
- `YourProjectName.svg`
- Previewed in your default browser, fully themed and grouped.

## 📦 Packaging

To compile with PyInstaller:

```bash
python -m PyInstaller --onefile --noconsole --icon=unrealuml_icon.ico run_all.py
```

> Be sure `plantuml.jar` is in the same folder.

## 🧑‍💻 Author

Developed by **Robson Franco Maciel** for Unreal Engine professionals, with clarity, documentation, and architecture visualization in mind.

---

## 📗 Versão em Português

**Uuml** é uma aplicação visual moderna feita em Python com `customtkinter`, que gera automaticamente diagramas UML a partir de projetos Unreal Engine em C++.

## 🔧 Funcionalidades

- Interface com botão "Gerar Tudo" e área de log ao vivo.
- Detecção automática da pasta `Source`.
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
2. Baixe o `plantuml.jar` de [https://plantuml.com/download](https://plantuml.com/download).
3. Coloque `plantuml.jar` na mesma pasta dos scripts.
4. Execute `run_all.py` ou o `.exe`.
5. O app irá:
   - Detectar a pasta `Source`
   - Gerar o `.puml`
   - Limpar o `.puml`
   - Renderizar o `.svg`
   - Abrir no navegador automaticamente

> Se o Java estiver desatualizado, o app abrirá o link correto para baixar o JDK 17.0.12 automaticamente.

## 📦 Empacotamento

```bash
python -m PyInstaller --onefile --noconsole --icon=unrealuml_icon.ico run_all.py
```

## 👤 Autor

Desenvolvido por **Robson Franco Maciel** para profissionais de Unreal Engine que precisam visualizar, documentar e entender a arquitetura de grandes projetos de forma clara.

## 🖼️ Logo

![Uuml Logo](images/logo.png)

---

**Uuml** nasceu para facilitar a leitura estrutural de grandes projetos Unreal. Ideal para documentação, times distribuídos, onboarding técnico e engenharia reversa visual.

