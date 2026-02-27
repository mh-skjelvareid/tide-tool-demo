# tide-tool-demo
A small example Python project which checks and visualizes Norwegian tide levels based on the Norwegian Mapping Authority's tide level API. The project is meant for educational purposes, demonstrating tools used in Python development.


## Pacakage management with UV
We're assuming that a git repository has already been created and that we have navigated to the root of the repository. The directory contains

    ├───.gitignore
    ├───LICENSE
    └───README.md

### Project initialization
To initialize a project structure as a package (to be installed / distributed), use

    uv init --package

This adds the following files and folders

    ├───src
    │   └───tide_tool_demo
    │       └─── __init__.py     
    ├───.python-version
    └───pyproject.toml

The src subfolder is where the Python code lives. The \__init__.py file is an empty file signalling that the code is a Python package. The .python-version file simply contains the python version number (for administering projects based on different versions). The pyproject.toml contains a lot of important metadata, for example the name of the project, the version, dependencies, build system, parameters for coding tools, etc.

### Virtual environment
To initialize a virtual environment, use 

    uv venv

This creates the subfolder .venv. The folder structure and content differs between different operating systems. For Windows the main parts looks like this: 

    └───.venv
        ├───Lib
        │   ├───site-packages
        │   └───...
        └───Scripts
           ├─── activate 
           └───...

The site-packages contains all external Python packages installed for the project.  


To activate the virtual environment, run the activate script.

    # Windows
    .\.venv\Scripts\activate
    # Linux / Mac
    source .venv/bin/Activate 

### Installing depdndencies (external packages)
To add dependencies, use uv add, e.g. 

    uv add requests matplotlib numpy mkdocs-material

This installs the dependencies into the virtual environment. The pyproject.toml file is updated with (e.g.)

    dependencies = [
        "matplotlib>=3.10.8",
        "numpy>=2.4.2",
        "requests>=2.32.5",
    ]

and a file called uv.lock is created. The file contains the details of the exact versions of all dependencies (including those installed indirectly via other dependencies). 


## Documentation with mkdocs
Create a new setup for MkDocs documentation with
    
    mkdocs new .

This creates 

- docs/index.md 
- mkdocs.yml

Documentation is written as MarkDown files in the docs subfolder. The mkdocs.yml file contains metadata (instructions on how documentation is built). Add the following to mkdocs.yml:

    plugins:
    - mkdocstrings:
        handlers:
            python:
            options:
                docstring_style: numpy
                docstring_options:
                ignore_init_summary: true
                members_order: source
                show_source: true
                show_signature: true

Let's create a file that automatically extracts docstring information and formats it as an API reference. First, open stc/tide_tool_demo/\__init__.py and add the following:

    from .tide_tool_demo import TideApiCaller, TideInfo
    \__all__ = ["TideInfo", "TideApiCaller"]

This exposes the API for the package. Then create docs/api.md and add the followiong line:

    ::: tide_tool_demo

