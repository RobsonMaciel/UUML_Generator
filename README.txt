# PlantUML Portable Viewer

Este pacote permite gerar diagramas UML a partir de arquivos .puml sem instalar nada.

## Como usar

1. Certifique-se de ter o Java instalado (Java 8 ou superior).
2. Clique duas vezes no arquivo `render.bat`.
3. Isso vai gerar um `example.png` com o diagrama UML.

Você pode substituir o `example.puml` por qualquer arquivo .puml seu.

## Observação

Este pacote não inclui o `plantuml.jar` por motivos de licenciamento.
Baixe o arquivo oficial em:
https://plantuml.com/download

Coloque o arquivo `plantuml.jar` na mesma pasta que `render.bat`.

Compilar via Powershell
& "C:\Users\Robson\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\Scripts\pyinstaller.exe" --onefile --noconsole --icon=unrealuml_icon.ico UnrealUML_Generator_fixed.py
