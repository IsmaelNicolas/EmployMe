# Configura la imagen base
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de requisitos a /app
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y gcc \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Excluye la carpeta env y copia el contenido de tu proyecto a /app
COPY . .

# Expone el puerto 8000 para que sea accesible desde fuera del contenedor
EXPOSE 8080

# Ejecuta el comando para iniciar tu aplicación
CMD ["python", "-u", "app.py"]
