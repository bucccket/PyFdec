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

I am very grateful there already exists a wrapper class for BytesIO that enables reading bits. However the way the library is written and the fact it doesn't seem well maintained has me worried. I want to reduce or alltogether remove any outside deps to ensure that this project can last on its own.
