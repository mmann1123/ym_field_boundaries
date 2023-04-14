# DOESN'T WORK!!!!!!!!! ARGH!!!!


# Ubuntu Linux 20.04
# AMI Deep learning AMI GPU PyTorch 1.13.1
# G3 instance but  P3, P3dn, P4d, G5, G4dn also work

# vs code ssh profile 
Host aws_mann_cultionet_v2
    HostName something.compute-1.amazonaws.com
    User ubuntu
    IdentityFile  


# one first setup
#conda config --set auto_activate_base false
conda init bash
source ~/.profile
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
pip install intel-openmp

# Install PyTorch Geometric and its dependencies
pip install \
    torch \
    torchvision \
    torchaudio  

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
sudo apt install python-pytest -y
cd cultionet/tests
pytest -vv

# mount flexible storage
# mkdir efs -p
# sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport fs-064b6369b27fcf25f.efs.us-east-1.amazonaws.com:/ efs


# docker file to run cultionet
FROM nvidia/cuda:11.6.0-base-ubuntu20.04

# Install GDAL
RUN apt update -y && \
    apt upgrade -y && \
    apt install software-properties-common -y && \
    add-apt-repository ppa:ubuntugis/ubuntugis-unstable -y && \
    apt update -y && \
    apt install \
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
    python-is-python3 \
    pip \
    git -y

ENV CPLUS_INCLUDE_PATH="/usr/include/gdal"
ENV C_INCLUDE_PATH="/usr/include/gdal"
ENV LD_LIBRARY_PATH="/usr/local/lib"
ENV PATH="/root/.local/bin:$PATH"

RUN pip install -U pip setuptools wheel
RUN pip install -U --no-cache-dir "setuptools>=59.5.0"
RUN pip install -U cython>=0.29.*
RUN pip install -U numpy>=1.22.0
RUN pip install intel-openmp

# Install PyTorch Geometric and its dependencies
RUN pip install \
    torch \
    torchvision \
    torchaudio --extra-index-url https://download.pytorch.org/whl/cu116

RUN TORCH_VERSION=`(python -c "import torch;print(torch.__version__)")` &&  pip install \
    torch-scatter \
    torch-sparse \
    torch-cluster \
    torch-spline-conv \
    torch-geometric --extra-index-url https://data.pyg.org/whl/torch-${TORCH_VERSION}.html

RUN GDAL_VERSION=$(gdal-config --version | awk -F'[.]' '{print $1"."$2"."$3}') && \
    pip install GDAL==$GDAL_VERSION --no-binary=gdal

# Install cultionet
RUN pip install --user cultionet@git+https://github.com/jgrss/cultionet.git
RUN git clone https://github.com/jgrss/cultionet.git
CMD /bin/bash

# try running on AWS instance?? 
# cp GWU_deep_learning_cultionet dockerfile
# docker build -t cultionet .
# docker images -a 
# docker run -v /home/ubuntu:/home  -it cultionet
# cd cultionet/tests
# pip install -U pytest
#pytest -vv
