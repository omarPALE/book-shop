
FROM ubuntu/nano-gcc:latest

RUN apt-get update && \
    apt-get install -y python3 python3-pip && apt-get install -y sudo && apt-get install -y curl

WORKDIR /home/

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip3 install requests






