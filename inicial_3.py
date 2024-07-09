import os, time
# Instalar con pip install flask
from flask import Flask, jsonify, request
# Instalar con pip install flask-cors
from flask_cors import CORS

"""
Para trabajar con archivos asegurar que un nombre de archivo 
proporcionado por el usuario sea seguro para guardarlo en el sistema de archivos.
"""
# Si es necesario, pip install Werkzeug 
from werkzeug.utils import secure_filename

from app.models.auto import Auto
from app.database import init_app, init_db

"""
Crear las dependencias
pip freeze > requirements.txt

Instalar todas las dependencias
pip install -r requirements.txt

"""
d = os.path.dirname(__file__)
os.chdir(d)

ruta_destino = 'static/img/'
if not os.path.exists(ruta_destino):
    os.makedirs(ruta_destino)


app = Flask(__name__)
CORS(app)

# Inicializar la base de datos con la aplicación Flask
init_app(app)

@app.route('/init-db')
def init_db_route():
    init_db()
    return "Base de datos inicializada correctamente."

@app.route('/')
def principal():
    return 'ahora siiii  #####'

@app.route('/autos', methods=['POST'])
def upload_auto():
    try:
        print("HOLAAAAAAAAAAAAAAA")
        data = request.form
        print("Request form data:", data)
        
        if 'foto' not in request.files:
            return jsonify({'message': 'No se encontró el archivo de imagen'}), 400

        archivo = request.files['foto']
        print(">>>>>>>>>>>>>>>>", data)
        print(">>>>>>>>>>>>>>>>", archivo)

        if archivo.filename == '':
            return jsonify({'message': 'No se seleccionó ningún archivo'}), 400

        nombre_imagen = secure_filename(archivo.filename)
        print(">>>>>>>>>>>>>>>>", nombre_imagen)

        nombre_base, extension = os.path.splitext(nombre_imagen)
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
        archivo.save(os.path.join(ruta_destino, nombre_imagen))

        required_fields = ['nombre', 'marca', 'modelo', 'dominio']
        for field in required_fields:
            if field not in data:
                print(f"Campo {field} faltante en data: {data}")
                return jsonify({'message': f"Campo {field} faltante"}), 400

        new_auto = Auto(
            nombre=data['nombre'],
            marca=data['marca'],
            modelo=data['modelo'],
            dominio=data['dominio'],
            foto=nombre_imagen,
        )
        new_auto.save()
        return jsonify({'message': 'Vehículo subido correctamente'}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Error al subir el vehículo', 'error': str(e)}), 500

@app.route('/autos', methods=['GET'])
def get_all_autos():
    autos = Auto.get_all()
    autos_json = [auto.serialize() for auto in autos]
    return jsonify(autos_json)

@app.route('/autos/<int:id>', methods=['GET'])
def get_by_id_auto(id):
    auto = Auto.get_by_id(id)
    if auto:
        return jsonify(auto.serialize())
    else:
        return jsonify({'message': 'Vehículo no encontrado'}), 404

@app.route('/autos/<int:id>', methods=['DELETE'])
def delete_auto(id):
    auto = Auto.get_by_id(id)
    if not auto:
        return jsonify({'message': 'Vehículo no encontrado'}), 404
    auto.delete()
    return jsonify({'message': 'El vehículo fue borrado'})

@app.route('/autos/<int:id>', methods=['PUT'])
def update_auto(id):
    auto = Auto.get_by_id(id)
    if not auto:
        return jsonify({'message': 'Vehículo no encontrado'}), 404
    data = request.form
    auto.nombre = data.get('nombre', auto.nombre)
    auto.marca = data.get('marca', auto.marca)
    auto.modelo = data.get('modelo', auto.modelo)
    auto.dominio = data.get('dominio', auto.dominio)
    auto.foto = data.get('foto', auto.foto)
    auto.save()
    return jsonify({'message': 'Vehículo actualizado correctamente'})

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000)