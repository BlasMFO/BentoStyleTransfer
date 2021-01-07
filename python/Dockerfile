FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -yq \
    && apt-get -yq install nano tree curl python3-pip \
	&& rm -rf /var/lib/apt/lists/*

RUN pip3 install Flask==1.1.2 requests==2.25.1 \
	--no-cache-dir
    
WORKDIR /app

COPY . /app

EXPOSE 80

CMD [ "python3", "app.py" ]