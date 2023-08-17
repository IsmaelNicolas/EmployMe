# Usamos una imagen base de Node.js
FROM node:16

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos de tu aplicación al directorio de trabajo en el contenedor
COPY package.json package-lock.json /app/

# Instalamos las dependencias
RUN npm install

# Copiamos el resto de los archivos
COPY . /app/

# Exponemos el puerto en el que se ejecutará la aplicación
EXPOSE 3000

# Comando para ejecutar la aplicación
CMD ["node", "index.js"]
