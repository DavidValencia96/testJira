from flask import Flask, render_template, send_from_directory, jsonify, request
from generate_report import generar_reporte_route
from project import obtener_proyectos
from issuesSprint import obtener_hus_de_sprint, obtener_sprints_jira  # Asegúrate de importar ambas funciones
import os, json
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/data/<filename>')
def download_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'data'), filename)

@app.route('/')
def index():
    if not os.path.exists('data/projects.json'):
        obtener_proyectos() 

    with open('data/projects.json', 'r') as file:
        proyectos = json.load(file)

    return render_template('index.html', proyectos=proyectos)

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
        return jsonify({"error": str(e)}), 500

@app.route('/obtener_hus', methods=['POST'])
def obtener_hus():
    try:
        data = request.get_json() 
        proyecto_id = data.get('proyecto_id')
        sprint_id = data.get('sprint_id')

        if not proyecto_id or not sprint_id:
            return jsonify({"error": "Faltan parámetros requeridos: proyecto_id o sprint_id"}), 400

        return obtener_hus_de_sprint(proyecto_id, sprint_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
