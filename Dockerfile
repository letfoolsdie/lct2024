# Start FROM Nvidia PyTorch image https://ngc.nvidia.com/catalog/containers/nvidia:pytorch
FROM nvcr.io/nvidia/pytorch:23.05-py3

# apt install required packages
RUN apt-get update
RUN apt-get install -y pkg-config 
RUN apt-get install -y ffmpeg libavformat-dev libavcodec-dev libswscale-dev 
# RUN apt-get update \
#     && apt-get install -y ffmpeg libsm6 libxext6 git ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 python3.8-dev default-libmysqlclient-dev libgtk2.0-dev pkg-config build-essential \
#     && apt install -y zip htop screen libgl1-mesa-glx \
#     && apt-get clean

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip3 install transformers[torch] qdrant-client fastapi sentence-transformers sacremoses
RUN pip3 install opencv-contrib-python==4.8.0.74 ffmpegcv

WORKDIR /app

