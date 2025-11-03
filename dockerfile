# pip install
FROM nvidia/cuda:12.1.0-base-ubuntu22.04 AS pip-install

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3.10 python3-pip python3.10-distutils && \
    rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/bin/python3.10 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# メイン
FROM nvidia/cuda:12.1.0-base-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3.10 python3-pip python3.10-distutils libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/bin/python3.10 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

ENV HOME=/app

WORKDIR /app

COPY --from=pip-install /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=pip-install /usr/lib/python3/dist-packages /usr/lib/python3/dist-packages

COPY ./src ./src
COPY ./resources ./resources

RUN mkdir -p ./.cache && chmod 777 ./.cache

CMD ["python", "src/main.py"]
