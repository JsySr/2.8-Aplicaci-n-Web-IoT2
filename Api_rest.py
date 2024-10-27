from flask import Flask, jsonify, request
from flask import Flask, render_template
import pymysql

app = Flask(__name__)

# Configuración de la conexión a la base de datos
db_config = {
    'host': 'instancia-db-iot.cv62ssqqmg30.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'Admin12345#!',
    'database': 'IoTCarStatus',
    'cursorclass': pymysql.cursors.DictCursor  # Para obtener resultados como diccionario
}

# Función para conectarse a la base de datos
def get_db_connection():
    return pymysql.connect(**db_config)

# Rutas CRUD

@app.route('/status', methods=['GET'])
def get_status():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM IoTCarStatus')
        statuses = cursor.fetchall()
    except pymysql.MySQLError as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()
    return jsonify(statuses)

@app.route('/status/<int:status_id>', methods=['GET'])
def get_status_by_id(status_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM IoTCarStatus WHERE id = %s', (status_id,))
        status = cursor.fetchone()
    except pymysql.MySQLError as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()
    
    if status:
        return jsonify(status)
    else:
        return jsonify({'error': 'Registro no encontrado'}), 404

@app.route('/status', methods=['POST'])
def create_status():
    new_status = request.json
    name = new_status.get('name')
    ip_client = new_status.get('ip_client')
    status = new_status.get('status')
    date = new_status.get('date')
    id_device = new_status.get('id_device')

    if not all([name, ip_client, status, date, id_device]):
        return jsonify({'error': 'Faltan datos'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO IoTCarStatus (name, ip_client, status, date, id_device) VALUES (%s, %s, %s, %s, %s)',
                       (name, ip_client, status, date, id_device))
        conn.commit()
        new_id = cursor.lastrowid
    except pymysql.MySQLError as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({'id': new_id, 'name': name, 'ip_client': ip_client, 'status': status, 'date': date, 'id_device': id_device}), 201

@app.route('/status/<int:status_id>', methods=['PUT'])
def update_status(status_id):
    updated_status = request.json
    name = updated_status.get('name')
    ip_client = updated_status.get('ip_client')
    status = updated_status.get('status')
    date = updated_status.get('date')
    id_device = updated_status.get('id_device')

    if not all([name, ip_client, status, date, id_device]):
        return jsonify({'error': 'Faltan datos'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE IoTCarStatus SET name = %s, ip_client = %s, status = %s, date = %s, id_device = %s WHERE id = %s',
                       (name, ip_client, status, date, id_device, status_id))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Registro no encontrado'}), 404
    except pymysql.MySQLError as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({'message': 'Registro actualizado correctamente'})

@app.route('/status/<int:status_id>', methods=['DELETE'])
def delete_status(status_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM IoTCarStatus WHERE id = %s', (status_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Registro no encontrado'}), 404
    except pymysql.MySQLError as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({'message': 'Registro eliminado correctamente'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Registros')
def otra_pagina():
    return render_template('Registros.html')





# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
