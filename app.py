from flask import Flask, render_template
from generate_report import generar_reporte_route  # Importar la función para la ruta de reporte
from project import obtener_proyectos  # Importar la función desde jira_utils.py

app = Flask(__name__)

# Ruta para servir el archivo HTML (index.html)
@app.route('/')
def index():
    proyectos = obtener_proyectos()  # Obtener los proyectos desde Jira
    return render_template('index.html', proyectos=proyectos)

# Llamamos a la función generar_reporte_route para registrar la ruta
generar_reporte_route(app)

if __name__ == '__main__':
    app.run(debug=True)
