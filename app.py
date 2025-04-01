from flask import Flask, render_template, send_from_directory, jsonify, request
from generate_report import generar_reporte_route
from project import obtener_proyectos
from issuesSprint import obtener_hus_de_sprint
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

@app.route('/obtener_hus', methods=['POST'])
def obtener_hus():
    data = request.get_json() 
    proyecto_id = data.get('proyecto_id')
    sprint_id = data.get('sprint_id')

    return obtener_hus_de_sprint(proyecto_id, sprint_id)

if __name__ == '__main__':
    app.run(debug=True)
