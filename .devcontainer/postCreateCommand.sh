#!/bin/sh
# postCreateCommand.sh

echo "START Install"

sudo apt update
sudo apt-get install cmake -y
sudo apt-get install git-lfs
sudo apt-get install zstd
sudo chown -R vscode:vscode .

# install vespa-cli
wget -O /tmp/vespa-cli.tgz https://github.com/vespa-engine/vespa/releases/download/v8.218.31/vespa-cli_8.218.31_linux_amd64.tar.gz
tar zxf /tmp/vespa-cli.tgz -C /tmp
sudo mv /tmp/vespa-cli_8.218.31_linux_amd64 /usr/local/vespa 
echo 'export PATH="/usr/local/vespa/bin:$PATH"' >> ~/.bashrc

# for python 
pip install poetry

poetry config virtualenvs.in-project true
poetry install --no-root
poetry run pip install git+https://github.com/rinnakk/japanese-clip.git
poetry run pre-commit install
VENV=`poetry env info -p`
echo "source ${VENV}/bin/activate" >> ~/.bashrc

# for frontend
cd frontend
. ${NVM_DIR}/nvm.sh
nvm install
yarn

echo "FINISH Install"