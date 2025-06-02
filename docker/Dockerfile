# Usar a imagem oficial do Python
FROM python:3.11

# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies 
# Instalação de dependências do sistema não necessariamente necessárias:
# Se você não estiver utilizando pacotes que exigem gcc, essa etapa 
# é desnecessária e pode aumentar o tamanho da imagem. 
RUN apt-get update && apt-get install -y gcc

# Copy requirements.txt and install dependencies
COPY ../requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create database directory
RUN mkdir -p /app/db

# Cloud Run vai passar a porta dinamicamente através da variável PORT
# Definimos um valor padrão para desenvolvimento local
ENV PORT=8000

# Apenas documenta que a aplicação usa a porta definida pela variável PORT
EXPOSE ${PORT}

# Run Django with Cloud Run compatibility using JSON format for CMD
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && gunicorn --bind 0.0.0.0:${PORT} --workers 2 app.wsgi:application"]