# ubuntu  linux  
# AMI Deep learning AMI GPU PyTorch 1.13.1
# G3 instance but  P3, P3dn, P4d, G5, G4dn also work

sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt-get update
sudo apt install ubuntu-drivers-common -y
ubuntu-drivers devices
sudo apt install nvidia-driver-465 -y


https://developer.nvidia.com/cuda-11.3.0-download-archive?target_os=Linux&target_arch=arm64-sbsa&Compilation=Cross&Distribution=Ubuntu&target_version=20.04
#linux
#arm64-sbsa
#cross
#ubuntu
#20.04
#deb local

wget https://developer.download.nvidia.com/compute/cuda/11.3.0/local_installers/cuda-repo-cross-sbsa-ubuntu2004-11-3-local_11.3.0-1_all.deb
sudo dpkg -i cuda-repo-cross-sbsa-ubuntu2004-11-3-local_11.3.0-1_all.deb
sudo apt-key add /var/cuda-repo-cross-sbsa-ubuntu2004-11-3-local/7fa2af80.pub
sudo apt-get update
sudo apt-get -y install cuda-cross-sbsa
 

#install pyenv
curl https://pyenv.run | bash


echo 'export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
' >> ~/.profile

exec "$SHELL"

echo 'export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if which pyenv > /dev/null; then eval "$(pyenv init --path)"; fi
if which pyenv > /dev/null; then eval "$(pyenv init -)"; fi
if which pyenv > /dev/null; then eval "$(pyenv virtualenv-init -)"; fi' >> ~/.bashrc

echo 'pyenv activate venv.cultionet' >> ~/.bashrc

source ~/.bashrc
exec "$SHELL"

sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev -y


pyenv install 3.8.12
pyenv virtualenv 3.8.12 venv.cultionet
pyenv activate venv.cultionet

# other reqs
pip install -U pip setuptools wheel "cython>=0.29.*" "numpy<=1.21.0"
# required to build GDAL Python bindings for 3.2.1
pip install --upgrade --no-cache-dir "setuptools<=58.*"

# pytorch 
pip install torch==1.10.1+cu113 torchvision==0.11.2+cu113 torchaudio==0.10.1+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html

sudo reboot


# more dependancies 
pip install torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric torch-geometric-temporal -f https://data.pyg.org/whl/torch-1.10.1+cu113.html

# install gdal
sudo add-apt-repository ppa:ubuntugis/ppa
sudo apt install build-essential
sudo apt update
sudo apt install libspatialindex-dev libgdal-dev gdal-bin -y

export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal

pip install GDAL==3.2.1

# install cultionet
git clone https://github.com/jgrss/cultionet.git
cd cultionet
pip install .






# not actually passing tests

# Ubuntu  linux  
# AMI Deep learning AMI GPU PyTorch 1.13.1
# G3 instance but  P3, P3dn, P4d, G5, G4dn also work


conda config --set auto_activate_base true
source activate pytorch

sudo apt update -y && \
    sudo apt upgrade -y && \
    sudo apt install software-properties-common -y && \
    sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable -y && \
    sudo apt update -y && \
    sudo apt install \
    build-essential \
    python3.8 \
    python3-pip \
    libgeos++-dev \
    libgeos-3.8.0 \
    libgeos-c1v5 \
    libgeos-dev \
    libgeos-doc \
    libspatialindex-dev \
    g++ \
    libgdal-dev \
    gdal-bin \
    libproj-dev \
    libspatialindex-dev \
    geotiff-bin \
    libgl1 \
    pip \
    git -y && \
    sudo apt upgrade -y 
 

export CPLUS_INCLUDE_PATH="/usr/include/gdal"
export C_INCLUDE_PATH="/usr/include/gdal"
export LD_LIBRARY_PATH="/usr/local/lib"


pip install testresources
pip install -U pip setuptools wheel
pip install -U --no-cache-dir "setuptools<=58.*"
pip install -U --no-cache-dir cython>=0.29.*
pip install -U --no-cache-dir "numpy>=1.21.0,<1.24"

# Install PyTorch Geometric and its dependencies
pip install \
    torch \
    torchvision \
    torchaudio --extra-index-url https://download.pytorch.org/whl/cu117

TORCH_VERSION=`(python -c "import torch;print(torch.__version__)")` &&
    pip install \
    torch-scatter \
    torch-sparse \
    torch-cluster \
    torch-spline-conv \
    torch-geometric -f https://data.pyg.org/whl/torch-${TORCH_VERSION}.html

GDAL_VERSION=$(gdal-config --version | awk -F'[.]' '{print $1"."$2"."$3}') && \
    pip install GDAL==$GDAL_VERSION --no-binary=gdal

# Install cultionet
pip install --user cultionet@git+https://github.com/jgrss/cultionet.git
git clone https://github.com/jgrss/cultionet.git
pip install testfixtures pytest
cd cultionet/tests
pytest -vv
