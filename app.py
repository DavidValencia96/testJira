from flask import Flask, render_template, send_from_directory
from generate_report import generar_reporte_route  # Importar la función para la ruta de reporte
from project import obtener_proyectos  # Importar la función desde jira_utils.py
import os, json
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Ruta para servir el archivo JSON desde la carpeta 'data'
@app.route('/data/<filename>')
def download_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'data'), filename)

# Ruta para la página principal
@app.route('/')
def index():
    # Obtenemos los proyectos solo si no han sido obtenidos aún
    if not os.path.exists('data/projects.json'):
        obtener_proyectos()  # Obtener los proyectos desde Jira

    # Cargar los proyectos desde el archivo JSON
    with open('data/projects.json', 'r') as file:
        proyectos = json.load(file)

    return render_template('index.html', proyectos=proyectos)

# Llamamos a la función generar_reporte_route para registrar la ruta
generar_reporte_route(app)

if __name__ == '__main__':
    app.run(debug=True)
