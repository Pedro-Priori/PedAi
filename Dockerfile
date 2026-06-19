# Usar a imagem oficial e leve do Python
FROM python:3.12-slim

# Evitar a criação de ficheiros residuais e forçar os logs no terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Definir a pasta de trabalho dentro do container
WORKDIR /app

# Copiar apenas os requisitos primeiro (otimiza o tempo de construção)
COPY requirements.txt /app/

# Instalar as dependências e o servidor Gunicorn
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copiar todo o resto do projeto para dentro do container
COPY . /app/

# Rodar as migrações do banco de dados (SQLite)
RUN python manage.py migrate

# Expor a porta que o Django vai usar
EXPOSE 8000

# Ligar o projeto usando o Gunicorn (apontando para o seu pedai_marketplace)
CMD ["gunicorn", "pedai_marketplace.wsgi:application", "--bind", "0.0.0.0:8000"]
