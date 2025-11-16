FROM python:3.9-slim

WORKDIR /app

# Instalar solo dependencias esenciales
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero para cache de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crear estructura de directorios
RUN mkdir -p frontend backend shared_data sample_data

# Copiar código
COPY frontend/ ./frontend/
COPY backend/ ./backend/
COPY sample_data/ ./sample_data/

EXPOSE 8501

HEALTHCHECK CMD curl -f http://localhost:8501/_stcore/health

# Usar CMD en lugar de ENTRYPOINT para permitir override en docker-compose
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.runOnSave=true", "--server.fileWatcherType=poll"]