# tide-tool-demo
A small example Python project which checks and visualizes Norwegian tide levels based on the Norwegian Mapping Authority's tide level API. The project is meant for educational purposes, demonstrating tools used in Python development.


## Pacakage management with UV
We're assuming that a git repository has already been created and that we have navigated to the root of the repository. The directory contains

    ├───.gitignore
    ├───LICENSE
    └───README.md

To initialize a project structure as a package (to be installed / distributed), use

    uv init --package

This adds the following files and folders


    ├───src
    │   └───tide_tool_demo
    │       └─── __init__.py     
    ├───.python-version
    └───pyproject.toml

To initialize a virtual environment, use 

    uv venv

This creates the subfolder .venv 

    └───.venv
        ├───Lib
        │   ├───site-packages
        │   └───...
        └───Scripts
           ├─── activate 
           └───...

To add dependencies, use uv add, e.g. 

    uv add requests matplotlib numpy

This installs the dependencies into the virtual environment. The pyproject.toml file is updated with (e.g.)

    dependencies = [
        "matplotlib>=3.10.8",
        "numpy>=2.4.2",
        "requests>=2.32.5",
    ]

and a file called uv.lock is created. The file contains the details of the exact versions of all dependencies (including those installed indirectly via other dependencies). 
