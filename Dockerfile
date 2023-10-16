# Usa una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requisitos e instala las dependencias
RUN pip install Flask
RUN pip install Flask-PyMongo
RUN pip install pandas
RUN pip install Werkzeug
RUN pip install python-dotenv

# Copia el código de la aplicación
COPY ./app .

# Ejecuta la aplicación
CMD ["python","-u","main.py"]
