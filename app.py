import os
import json
import time
import logging
from config import Config
from flask import Flask, render_template, send_from_directory, jsonify, request
from generate_report import generar_reporte_route
from project import obtener_proyectos
from issuesSprint import obtener_hus_de_sprint, obtener_sprints_jira, generar_json_issues
from navigationProject import fetch_all_boards

app = Flask(__name__)
app.config.from_object(Config)

logging.basicConfig(level=logging.DEBUG)

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    total_time = time.time() - request.start_time
    if total_time > app.config.get('TIMEOUT', 130):
        return jsonify({"error": f"Tiempo de espera excedido ({total_time:.2f} segundos)"}), 504
    return response

@app.route('/data/<filename>')
def download_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'data'), filename)

@app.route('/')
def index():
    if not os.path.exists('data/projects.json'):
        obtener_proyectos()

    with open('data/projects.json', 'r') as file:
        proyectos = json.load(file)

    if not os.path.exists('data/boards.json'):
        fetch_all_boards()

    with open('data/boards.json', 'r') as file:
        boards = json.load(file)

    return render_template('index.html')

generar_reporte_route(app)

@app.route('/actualizar_sprints', methods=['POST'])
def actualizar_sprints():
    proyecto_id = request.json.get('proyecto_id')
    if not proyecto_id:
        return jsonify({"error": "Se requiere el ID del proyecto"}), 400

    try:
        sprints_data = obtener_sprints_jira(proyecto_id)
        return jsonify({"message": "Sprints actualizados correctamente", "data": sprints_data}), 200
    except Exception as e:
        logging.error(f"Error al actualizar sprints: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/obtener_hus', methods=['POST'])
def obtener_hus():
    try:
        data = request.get_json() 
        proyecto_id = data.get('proyecto_id')
        proyecto_key = data.get("projectKey")
        sprint_id = data.get('sprint_id')

        if not proyecto_id or not sprint_id or not proyecto_key:
            return jsonify({"error": "Faltan parámetros requeridos: proyecto_id, sprint_id o projectKey"}), 400

        logging.info(f"Generando JSON de issues para el proyecto: {proyecto_key}")
        generar_json_issues(proyecto_key)

        logging.info(f"Obteniendo HUs para el proyecto {proyecto_key}, sprint {sprint_id}")
        return obtener_hus_de_sprint(proyecto_id, sprint_id)

    except Exception as e:
        logging.error(f"Error al obtener HUs: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/obtener_tableros', methods=['GET'])
def obtener_tableros():
    try:
        fetch_all_boards() 
        return jsonify({"message": "Tableros obtenidos y guardados correctamente."}), 200
    except Exception as e:
        logging.error(f"Error al obtener tableros: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
