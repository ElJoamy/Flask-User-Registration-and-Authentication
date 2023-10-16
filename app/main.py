from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
import hashlib
import re
from dotenv import load_dotenv
import pandas as pd
from werkzeug.utils import secure_filename
import os
from bson import ObjectId

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
client = MongoClient("mongodb", 27017)  # Nombre del servicio de MongoDB en el archivo docker-compose.yml

db = client["user_db"]
collection = db["users"]

# Ruta al archivo CSV de países
df = pd.read_csv(os.environ.get('RUTA_CSV_PAISES'))

# Configuración para la subida de archivos
app.config["UPLOAD_FOLDER"] = os.environ.get('UPLOAD_FOLDER')
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])


ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

def is_valid_country_code(country_code):
    if country_code in df[' phone_code'].tolist():
        return True
    return False

# Función para hashear la contraseña
def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()

# Define una función para validar la contraseña
def is_valid_password(password):
    # Verifica que la contraseña tenga al menos 8 caracteres
    if len(password) < 8:
        return False

    # Verifica si la contraseña incluye al menos un carácter especial
    if not re.search(r'[!@#$%^&*(),.?":{}|<>-]', password):
        return False

    # Verifica si la contraseña incluye al menos una mayúscula
    if not re.search(r'[A-Z]', password):
        return False

    # Verifica si la contraseña incluye al menos un número
    if not re.search(r'[0-9]', password):
        return False

    return True

# Función para verificar si la extensión de un archivo es válida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            email = data['email']
            raw_password = data['password']
            username = data['username']
            country_code = data.get('codigo_de_pais', '')
        else:
            data = request.form
            email = data['email']
            raw_password = data['password']
            username = data['username']
            country_code = data.get('codigo_de_pais', '')

        if '@' not in email:
            return jsonify({'message': 'El correo electrónico no es válido'}), 400

        if not is_valid_password(raw_password):
            return jsonify({'message': 'La contraseña no cumple con los criterios'}), 400

        if country_code and not is_valid_country_code(country_code):
            return jsonify({'message': 'El código de país no es válido'}), 400

        imagen_perfil = request.files['imagen_perfil']
        if imagen_perfil and allowed_file(imagen_perfil.filename):
            filename = secure_filename(imagen_perfil.filename)
            imagen_perfil.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return jsonify({'message': 'Tipo de archivo no permitido para la imagen de perfil o ningún archivo proporcionado'}), 400

        hashed_password = hash_password(raw_password)

        users_collection = db.users

        user_data = {
            'email': email,
            'password': hashed_password,
            'username': username,
            'nombres': data.get('nombres', ''),
            'apellidos': data.get('apellidos', ''),
            'codigo_de_pais': country_code,
            'telefono': data.get('telefono', ''),
            'edad': data.get('edad', ''),
            'profesion': data.get('profesion', ''),
            'imagen_perfil': os.path.join(app.config['UPLOAD_FOLDER'], filename),
        }

        result = users_collection.insert_one(user_data)
        new_user_id = str(result.inserted_id)

        return jsonify({'message': 'Usuario registrado exitosamente', 'user_id': new_user_id})

    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username_or_email = data['username_or_email']
            password = data['password']
        else:
            data = request.form
            username_or_email = data['username_or_email']
            password = data['password']

        users = db.users
        user = users.find_one({'$or': [{'username': username_or_email}, {'email': username_or_email}]})

        if user and user['password'] == hashlib.sha256(password.encode()).hexdigest():
            # Usuario autenticado con éxito
            return jsonify({'message': 'Inicio de sesión exitoso'})
        else:
            return jsonify({'message': 'Credenciales incorrectas'}), 401

    return render_template('login.html')

@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    if request.is_json:
        data = request.get_json()
        user_id = ObjectId(user_id)

        existing_user = db.users.find_one({'_id': user_id})

        if existing_user:
            updated_data = {}

            if 'username' in data:
                updated_data['username'] = data['username']

            if 'email' in data:
                # Validar la dirección de correo electrónico
                if '@' not in data['email']:
                    return jsonify({'message': 'El correo electrónico no es válido'}), 400
                updated_data['email'] = data['email']

            if 'password' in data:
                # Validar la contraseña utilizando la función personalizada
                if not is_valid_password(data['password']):
                    return jsonify({'message': 'La contraseña no cumple con los criterios'}), 400
                updated_data['password'] = hash_password(data['password'])

            if 'imagen_perfil' in data:
                # Validar la imagen de perfil que sea jpg o jpeg
                if not data['imagen_perfil'].endswith('.jpg') and not data['imagen_perfil'].endswith('.jpeg'):
                    return jsonify({'message': 'La imagen de perfil debe ser jpg o jpeg'}), 400
                updated_data['imagen_perfil'] = data['imagen_perfil']

            # Si se proporciona un valor para 'codigo_de_pais', valida su formato
            if 'codigo_de_pais' in data:
                country_code = data['codigo_de_pais']
                if country_code:
                    if not is_valid_country_code(country_code):
                        return jsonify({'message': 'El código de país no es válido'}), 400
                updated_data['codigo_de_pais'] = country_code

            # Actualiza los campos adicionales
            for key in ['nombres', 'apellidos', 'telefono', 'edad', 'profesion']:
                if key in data:
                    updated_data[key] = data[key]
                else:
                    updated_data[key] = existing_user.get(key, '')  # Utiliza el valor existente si no se proporciona en la solicitud

            # Realiza la actualización
            db.users.update_one({'_id': user_id}, {'$set': updated_data})

            return jsonify({'message': 'Usuario actualizado correctamente'})
        else:
            return jsonify({'message': 'Usuario no encontrado'}, 404)
    else:
        return jsonify({'message': 'Solicitud no válida, se esperaba JSON'}), 400

@app.route('/users', methods=['GET'])
def get_users():
    users_collection = db.users

    # Consulta todos los documentos de usuarios
    users = list(users_collection.find({}))

    # Convierte el ID de ObjectId de MongoDB a una cadena para su serialización
    for user in users:
        user['_id'] = str(user['_id'])

    return jsonify(users)

@app.route('/users', methods=['DELETE'])
def delete_all_users():
    users_collection = db.users

    # Elimina todos los usuarios
    result = users_collection.delete_many({})

    return jsonify({'message': f'Se eliminaron {result.deleted_count} usuarios'})

@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    users_collection = db.users

    # Convierte el user_id en ObjectId de MongoDB
    user_id = ObjectId(user_id)

    # Elimina el usuario por su ID
    result = users_collection.delete_one({'_id': user_id})

    if result.deleted_count == 1:
        return jsonify({'message': 'Usuario eliminado correctamente'})
    else:
        return jsonify({'message': 'Usuario no encontrado'}, 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
