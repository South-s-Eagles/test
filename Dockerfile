# Dockerfile
FROM python:3.10-slim

# Atualiza os pacotes e instala as dependências necessárias
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala uma versão mais recente do OpenSSL
RUN curl -O https://www.openssl.org/source/openssl-1.1.1l.tar.gz && \
    tar -xzvf openssl-1.1.1l.tar.gz && \
    cd openssl-1.1.1l && \
    ./config && make && make install && \
    cd .. && rm -rf openssl-1.1.1l*

# Define o diretório de trabalho
WORKDIR /app

# Copia o script Python e o arquivo requirements.txt para o contêiner
COPY . /app

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Define o comando de entrada padrão para o contêiner
CMD ["python", "webcrawler.py"]