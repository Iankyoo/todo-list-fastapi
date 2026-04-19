FROM python:3.13-slim 

ENV POETRY_VIRTUALENVS_CREATE=false 

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Instala poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Copia arquivos de dependência
COPY pyproject.toml poetry.lock ./

# Instala dependências
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --without dev --no-root

# Copia o resto da aplicação
COPY . .

# Garante permissão de execução
RUN chmod +x entrypoint.sh

# Expõe porta
EXPOSE 8000

# 🚀 Usa o entrypoint (ESSENCIAL)
CMD ["./entrypoint.sh"]