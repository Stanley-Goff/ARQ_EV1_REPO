# Utilizar Python 3.12 sobre una imagen slim
FROM python:3.12-slim

#Evitar archivos bytecode y activar salida inmediata
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#Establecer el directorio de trabajo
WORKDIR /app

#Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copiar el código de la aplicación
COPY . .

#Preparar el directorio de persistencia
RUN mkdir -p /app/data

#Documentar el puerto de la aplicación
EXPOSE 8000

#Ejecutar migraciones y levantar Django
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]