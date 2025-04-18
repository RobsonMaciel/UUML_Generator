# Uuml – Universal UML Diagram Generator

## Overview

Uuml é um aplicativo visual multiplataforma para gerar automaticamente diagramas UML de projetos em C++, C# (Unity), Python, Unreal Engine e outros. Ideal para visualizar, documentar e entender rapidamente a arquitetura de qualquer projeto.

---

## Key Features

- Suporte a múltiplas linguagens: C++, C++ Unreal Engine, C#, C# Unity, Python, Java (em breve)
- Extração automática de classes, métodos, atributos, structs, enums e interfaces
- Agrupamento inteligente por pacote, estereótipo ou módulo, com cores vivas
- Visual moderno (dark), texto branco, bordas coloridas, setas claras e layout otimizado
- Sem duplicidade de classes ou conflitos de nomes
- Log em tempo real de progresso e erros
- Exportação com um clique para `.puml` e `.svg`
- Modular e fácil de estender para novas linguagens
- Funciona no Windows, Mac e Linux

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

- Fundo escuro, fontes brancas, cores vivas para pacotes/classes
- Python: cada módulo é um pacote colorido, classes com <<PythonClass>>
- Unreal/Unity: agrupamento por estereótipo (ex: MonoBehaviour), cada um com cor própria
- Setas suaves, espaçamento otimizado, agrupamento claro
- Todo texto dentro das caixas é branco para máximo contraste

---

## Como usar

1. Instale **Java 17+** (necessário para renderizar PlantUML)
2. Instale **Python 3.9+** (se for usar scripts)
3. Instale o pacote Python:
   - `tkinter`
4. Baixe ou clone este repositório
5. Acesse a pasta `src`
6. Execute `UumlCentralApp.py` (ou o executável `.exe`)
7. Selecione o diretório do projeto e a linguagem alvo
8. Clique em "Generate" para gerar o diagrama UML

### Linha de comando

Também é possível gerar diagramas via terminal:

```bash
python src/UumlCentralApp.py --project caminho/para/UnrealProject --tipo cpp4ue
python src/UumlCentralApp.py --project caminho/para/UnityProject --tipo unity
python src/UumlCentralApp.py --project caminho/para/PythonProject --tipo python
```

- O arquivo `.puml` será gerado na raiz do projeto.
- Se Java e PlantUML estiverem disponíveis, o `.svg` será gerado e aberto automaticamente.
- Para Unreal Engine, um `entities.txt` também é criado com todas as entidades detectadas.

---

## Estrutura do Projeto

```
/Uuml
  /src
    UumlCentralApp.py
    CSharpForUnity.py
    CPPForUnrealEngine.py
    # ...outros módulos
    plantuml.jar
    unrealuml_icon.ico
  /CodeExamples
  README.md, LICENSE, etc.
```

---

## Requisitos

- **Python 3.9+**
- **Java 17+**
- Pacote Python: `tkinter`

> Se o Java estiver ausente/desatualizado, o app vai orientar a instalar o JDK 17.

---

## Executável Standalone

Para criar um executável (Windows):

```bash
pip install pyinstaller
cd src
pyinstaller --onefile --noconsole --icon=unrealuml_icon.ico UumlCentralApp.py
```
- O executável estará em `dist/UumlCentralApp.exe`.
- Inclua o `plantuml.jar` na mesma pasta do executável.

---

## O que já faz

- Suporte a C++, C++ Unreal Engine, C# (Unity), Python
- Geração automática de classes, métodos, atributos, structs, enums e interfaces
- Agrupamento visual inteligente por pacote, estereótipo ou módulo
- Visual moderno, diagramas prontos para documentação
- Exportação fácil para PlantUML e SVG
- Modular e pronto para novas linguagens

---

## O que será implementado

- Suporte completo a Java
- Suporte aprimorado a Blueprints do Unreal Engine
- Mais opções de customização visual
- Suporte a outros tipos de diagramas UML

---

## Autor & Créditos

Desenvolvido por **Robson Franco Maciel** e colaboradores.

- **PlantUML**: Diagramas por [PlantUML](https://plantuml.com/)

---

## 🖼️ Logo

![Uuml Logo](images/logo.png)

---

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE).

---

Uuml é ideal para documentação, onboarding, equipes distribuídas e engenharia reversa visual de qualquer código!
