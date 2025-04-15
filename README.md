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
3. Run `UnrealUML_APP.py` (or the compiled `.exe`).
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

## 📥 How to Get `plantuml.jar`

The UnrealUML Generator uses [PlantUML](https://plantuml.com/) to convert `.puml` files into visual diagrams.

To obtain `plantuml.jar`:

1. Visit the official PlantUML download page: https://plantuml.com/download
2. Download the file `plantuml.jar`.
3. Place the file in the same directory as the `UnrealUML_Generator.exe` or script.

> 💡 PlantUML is an open-source tool developed by Arnaud Roques. All credits to the original authors. For more, visit: https://plantuml.com

## 🔍 Output Example

- `YourProjectName.puml`
- `YourProjectName.svg`
- Previewed in your default browser, fully themed and grouped.

## 📦 Packaging

To compile with PyInstaller:

```bash
python -m PyInstaller --onefile --noconsole --icon=unrealuml_icon.ico UnrealUML_APP.py
```

> Be sure `plantuml.jar` is in the same folder.

## 🧑‍💻 Author

Developed by **Robson Franco Maciel** for Unreal Engine professionals, with clarity, documentation, and architecture visualization in mind.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

© 2025 Robson Franco Maciel. Please include proper attribution when using this tool.

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
4. Execute `UnrealUML_APP.py` ou o `.exe`.
5. O app irá:
   - Detectar a pasta `Source`
   - Gerar o `.puml`
   - Limpar o `.puml`
   - Renderizar o `.svg`
   - Abrir no navegador automaticamente

> Se o Java estiver desatualizado, o app abrirá o link correto para baixar o JDK 17.0.12 automaticamente.

## 📥 Obter `plantuml.jar`

O UnrealUML Generator utiliza o [PlantUML](https://plantuml.com/) para converter arquivos `.puml` em diagramas visuais.

Para obter o `plantuml.jar`:

1. Acesse a página oficial de download: https://plantuml.com/download
2. Baixe o arquivo `plantuml.jar`
3. Coloque o arquivo na mesma pasta dos scripts ou do executável

> 💡 O PlantUML é uma ferramenta open-source desenvolvida por Arnaud Roques. Todos os créditos aos autores originais. Mais em: https://plantuml.com

## 📦 Empacotamento

```bash
python -m PyInstaller --onefile --noconsole --icon=unrealuml_icon.ico UnrealUML_APP.py
```

## 👤 Autor

Desenvolvido por **Robson Franco Maciel** para profissionais de Unreal Engine que precisam visualizar, documentar e entender a arquitetura de grandes projetos de forma clara.

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

© 2025 Robson Franco Maciel. Por favor, inclua os devidos créditos ao utilizar esta ferramenta.

## 🖼️ Logo

![Uuml Logo](images/logo.png)

---

**Uuml** nasceu para facilitar a leitura estrutural de grandes projetos Unreal. Ideal para documentação, times distribuídos, onboarding técnico e engenharia reversa visual.
