FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -yq \
    && apt-get -yq install nano tree tar wget curl python3-pip \
	&& rm -rf /var/lib/apt/lists/*

RUN mkdir /models && mkdir /models/tftransfer && mkdir /temp && \
    wget "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2?tf-hub-format=compressed" && \
    tar -C /models/tftransfer -zxvf ./2* && rm -f 2*

RUN pip3 install tensorflow==2.4.0 \
    opencv-python==4.4.0.44 scikit-learn==0.23.2 \
    scipy==1.5.3 Pillow==8.0.1 h5py==2.10.0 \
    matplotlib==3.3.2 pandas==1.1.3 \
    protobuf==3.13.0 regex==2020.10.23 BentoML==0.10.1 \
	--no-cache-dir

WORKDIR /app

COPY . /app

RUN python3 serve.py

EXPOSE 5000

CMD [ "bentoml", "serve", "-q", "--enable-microbatch", "TfModelService:latest" ]