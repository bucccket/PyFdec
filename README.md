# PyFdec

Python based flash decompilation module

# Contributing

## Poetry setup
The detailed installation guide for poetry [can be found here](https://python-poetry.org/docs/#installing-with-pipx).
After installing poetry, to get started just run: 
```bash
poetry run python -m venv .venv
poetry install
```
for testing run 
```python
poetry run pytest
```

## Working on NixOS or using Nix
enter development env by typing 
```bash
nix develop
```

# Plans For The Future

## BitIO

I am grateful that there is already a wrapper class for BytesIO that allows for reading bits. However, the way the library is written, along with the fact that it doesn't seem well-maintained, raises concerns. I want to minimize, or ideally eliminate, any external dependencies to ensure the long-term sustainability of this project.
