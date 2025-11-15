# メイン
FROM nvidia/cuda:12.1.0-base-ubuntu22.04

ARG USER_ID=1000
ARG GROUP_ID=1000
ARG USER_NAME=app

RUN groupadd -g ${GROUP_ID} ${USER_NAME} && \
    useradd -m -u ${USER_ID} -g ${GROUP_ID} ${USER_NAME}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3.10 python3-pip python3.10-distutils libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/bin/python3.10 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

ENV HOME=/app

RUN mkdir -p /app && chown -R ${USER_NAME}:${GROUP_ID} /app

WORKDIR /app

USER ${USER_NAME}

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./src ./src
COPY ./resources ./resources
COPY ./alembic.ini ./alembic.ini

RUN mkdir -p ./.cache && chmod 777 ./.cache

CMD ["python", "src/main.py"]
