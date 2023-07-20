#!/bin/sh
# postCreateCommand.sh

echo "START Install"

sudo apt update
sudo apt-get install cmake -y
sudo apt-get install git-lfs
sudo chown -R vscode:vscode .

pip install poetry

poetry config virtualenvs.in-project true
poetry install --no-root
poetry run pip install git+https://github.com/rinnakk/japanese-clip.git
poetry run pre-commit install

echo "FINISH Install"