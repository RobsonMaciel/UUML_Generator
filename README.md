# UnrealUML Generator

## 📘 English Version

**UnrealUML Generator** is a cross-platform visual application written in Python with a `customtkinter` interface, designed to automatically generate UML diagrams from the source code of an Unreal Engine project.

## 🔧 Features

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

## 🌟 Visual Style (PlantUML)

- Dark background (`#1e1e1e`), white fonts for contrast.
- Light blue color palette for borders and arrows (`#00bfff`).
- Classes grouped into logical packages (HUD, Actors, Controllers, etc).
- Consistent fonts for classes, methods, and attributes.
- Vertical layout with orthogonal lines (`top to bottom`, `linetype ortho`).

## 🚀 How to Use

1. Run `UnrealUML_Generator.exe` (or run the Python script directly if preferred).
2. The `Source` folder will be auto-detected. If needed, change it manually.
3. Click **"Generate Diagram"**.
4. The app will generate `YourProject.puml` and convert it into `YourProject.svg`.
5. The SVG will open automatically in your default browser.

> ⚠️ Requires `plantuml.jar` in the same folder as the executable/script to generate the image.

## 🛠 Requirements

- Python 3.9+ (if using script version)
- Java installed (to run `plantuml.jar`)
- Python libraries:
  - `customtkinter`
  - `tkinter`

## 🔍 Output Example

- `UnrealProjectName.puml`
- `UnrealProjectName.svg`
- Automatically opens the image with classes grouped by package

## 🧑‍💻 Author

Developed by [Robson Franco Maciel] focused on Unreal Engine projects.

## 📦 Packaging with PyInstaller

To package the app as a `.exe`, use the following generic command:

```bash
pyinstaller --onefile --noconsole --icon=unrealuml_icon.ico UnrealUML_Generator.py
```

To force a full rebuild (clean cache):

```bash
pyinstaller --onefile --noconsole --clean --icon=unrealuml_icon.ico UnrealUML_Generator.py
```

> Make sure you are in the same folder as the script and that `plantuml.jar` is available.

---

## 📗 Versão em Português

**UnrealUML Generator** é uma aplicação visual multiplataforma feita em Python com interface `customtkinter`, projetada para gerar diagramas UML automaticamente a partir do código-fonte de um projeto Unreal Engine.

## 🔧 Funcionalidades

- Interface visual para selecionar a pasta `Source` do projeto.
- Detecta automaticamente a pasta `Source` ao iniciar.
- Extrai automaticamente:
  - Classes (baseadas em `UCLASS`)
  - Métodos (baseados em `UFUNCTION`)
  - Atributos (baseados em `UPROPERTY`)
- Identifica o nome e a versão do projeto Unreal (.uproject).
- Gera um arquivo `.puml` organizado em pacotes por tipo de classe:
  - `GameModes`, `Characters`, `Controllers`, `Components`, etc.
- Cria relações de dependência entre classes que utilizam atributos de outra classe.
- Renderiza a imagem UML final no formato **SVG** com tema escuro.
- Abre automaticamente o SVG no navegador padrão após a geração.

## 🌟 Estilo Visual (PlantUML)

- Fundo escuro (`#1e1e1e`), fontes brancas para contraste.
- Paleta de cores azul-claro para bordas e setas (`#00bfff`).
- Classes agrupadas em pacotes lógicos (HUD, Actors, Controllers, etc).
- Fontes consistentes para classes, métodos e atributos.
- Layout vertical com linhas ortogonais (`top to bottom`, `linetype ortho`).

## 🚀 Como Usar

1. Execute `UnrealUML_Generator.exe` (ou o script Python diretamente, se preferir).
2. A pasta `Source` será detectada automaticamente. Se necessário, altere manualmente.
3. Clique em **"Gerar Diagrama"**.
4. O app gerará `SeuProjeto.puml` e o converterá em `SeuProjeto.svg`.
5. O SVG será aberto automaticamente no navegador padrão.

> ⚠️ Requer `plantuml.jar` na mesma pasta que o executável/script para gerar a imagem.

## 🛠 Requisitos

- Python 3.9+ (se for usar via script)
- Java instalado (para executar o `plantuml.jar`)
- Bibliotecas Python:
  - `customtkinter`
  - `tkinter`

## 🔍 Exemplo de Saída

- `UnrealProjectName.puml`
- `UnrealProjectName.svg`
- A imagem abre automaticamente com as classes organizadas por pacote

## 🧑‍💻 Autor

Desenvolvido por [Robson Franco Maciel] com foco em projetos Unreal Engine.

## 📦 Empacotamento com PyInstaller

Para empacotar o app como `.exe`, utilize o seguinte comando genérico:

```bash
pyinstaller --onefile --noconsole --icon=unrealuml_icon.ico UnrealUML_Generator.py
```

Para forçar uma recompilação completa (limpeza de cache):

```bash
pyinstaller --onefile --noconsole --clean --icon=unrealuml_icon.ico UnrealUML_Generator.py
```

> Certifique-se de estar na mesma pasta do script e com o `plantuml.jar` disponível.

---
**UnrealUML Generator** é uma ferramenta que facilita a compreensão estrutural de projetos Unreal Engine. Ideal para documentação, onboarding de equipes e visualização rápida da arquitetura geral do jogo.

