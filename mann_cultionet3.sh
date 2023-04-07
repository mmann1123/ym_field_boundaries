Ubuntu
Deep learning AMI GPU pytorch 1.13.1 Ubuntu 20.04
g3.4xlarge


fixed IP: 54.210.149.151

# skipping CUDA install 

mamba create --name cultionet --clone pytorch -y
exec "$SHELL"

echo 'conda activate cultionet' >> ~/.bashrc
source ~/.bashrc
exec "$SHELL"

 

# this seems to break things
#sudo apt install ubuntu-drivers-common
#sudo add-apt-repository ppa:graphics-drivers/ppa
#sudo apt-get update
#sudo apt install ubuntu-drivers-common
#sudo apt install nvidia-driver-465
#ubuntu-drivers devices

# problem CUDA 11.7 installed not 11.3
nvcc --version

# got oldest compatable vesrion with CUDA 11.7 https://pytorch.org/get-started/previous-versions/ 
mamba install pytorch==1.13.0 torchvision==0.14.0 torchaudio==0.13.0 pytorch-cuda=11.7 -c pytorch -c nvidia -y

python -c "import torch;print(torch.cuda.is_available())"

mamba install torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric torch-geometric-temporal -c pytorch -c nvidia -y

 
python -c "import torch;print(torch.cuda.is_available())"
