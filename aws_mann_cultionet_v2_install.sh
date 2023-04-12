# Ubuntu Linux 20.04
# AMI Deep learning AMI GPU PyTorch 1.13.1
# G3 instance but  P3, P3dn, P4d, G5, G4dn also work

# vs code ssh profile 
Host aws_mann_cultionet
    HostName something.compute-1.amazonaws.com
    User ubuntu
    IdentityFile  


# one first setup
#conda config --set auto_activate_base false
echo "conda activate pytorch" >> ~/.bashrc
source ~/.bashrc

# set up git
git config --global user.name "mmann1123"
git config --global  user.email "mmann1123@gmail.com"


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
pip install testfixtures
cd cultionet/tests
pytest -vv

# mount flexible storage
# mkdir efs -p
# sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport fs-064b6369b27fcf25f.efs.us-east-1.amazonaws.com:/ efs