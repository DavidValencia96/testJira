import requests
import base64
import time
import os
import csv  # Importamos la librería csv
import json  # Asegúrate de importar json
from flask import jsonify, request

# Función para generar el reporte
def generar_reporte(proyecto):
    # Datos de autenticación y configuración
    email = "pablo.munoz@bebolder.co"
    api_token = "ATATT3xFfGF0UrsshZ9JZEMG-0eZQbBJ_GgT5-mSghYU8ustURw07LprkdngoC1iO8Y198B4b8nIePIekKQNhL4uQAQsVeIXhpWRY3GjtN_O-j9zOS_ZixxwZPdzcqdVsw_SKfox8okJwcj_57XIu3ZM0C7iwDFD3E-vnkLo6TQpfL-i_3mV6jM=07B92C26"
    jira_domain = "https://bebolder.atlassian.net"

    # Autenticación base64
    auth_string = f"{email}:{api_token}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()

    # Parámetros de la consulta
    start_at = 0
    max_results = 100
    total = 0

    # Definir el JQL query
    jql_query = f"project={proyecto}"

    # Función para obtener los issues
    def obtener_issues_jira():
        nonlocal start_at, total
        while start_at < total or total == 0:
            url = f"{jira_domain}/rest/api/3/search?jql={jql_query}&startAt={start_at}&maxResults={max_results}"
            headers = {
                "Authorization": f"Basic {encoded_auth}",
                "Accept": "application/json"
            }
            
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Si la respuesta tiene un error, levantará una excepción
                json_response = response.json()
                total = json_response['total']
                
                # Guardar los datos JSON en un archivo
                with open(f"data/issues_{proyecto}.json", "a") as json_file:
                    json.dump(json_response, json_file, indent=4)  # Escribe la respuesta JSON de manera legible
                
                # Escribir los datos en el archivo CSV
                with open(f"data/issues_{proyecto}.csv", mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    
                    # Escribir solo los encabezados una vez
                    if start_at == 0:
                        writer.writerow(["Clave", "Resumen", "Estado", "Asignado a", "Creado", "story point", "HU padre", "issuetype"])

                    for issue in json_response['issues']:
                        key = issue['key']
                        summary = issue['fields']['summary']
                        status = issue['fields']['status']['name']
                        
                        # Verificamos si el campo 'assignee' está presente y no es None
                        assignee = issue['fields'].get('assignee')
                        assignee_name = assignee['displayName'] if assignee else "No asignado"
                        created = issue['fields']['created']
                        storyP = issue['fields'].get('customfield_10016', None) 
                        if not storyP: 
                            storyP = "N/A"
                        parent = issue['fields']['priority'].get('name', None) 
                        if not parent: 
                            parent = "N/A"
                        issuetype = issue['fields']['issuetype'].get('name', None) 
                        if not issuetype: 
                            issuetype = "N/A"
                        
                        # Añadimos la fila con los datos
                        writer.writerow([key, summary, status, assignee_name, created, storyP, parent, issuetype])
                
                start_at += max_results

            except requests.exceptions.RequestException as e:
                return jsonify({"error": f"Error en la extracción de datos: {e}"}), 500

        print(f"Datos extraídos exitosamente para el proyecto {proyecto}")

    # Medir el tiempo de ejecución
    start_time = time.time()

    # Llamar a la función para obtener los issues
    obtener_issues_jira()

    # Calcular el tiempo que tardó el proceso
    end_time = time.time()
    execution_time = end_time - start_time

    # Devolver la ruta del archivo y el tiempo de ejecución
    return {"archivo": f"data/issues_{proyecto}.csv", "tiempo": execution_time}

# Ruta para manejar la generación del reporte
def generar_reporte_route(app):
    @app.route('/generar_reporte', methods=['POST'])
    def reporte_route():
        data = request.get_json()  # Obtener los datos enviados por el formulario
        proyecto = data['proyecto']

        # Llamamos a la función generar_reporte de generate_report.py
        resultado = generar_reporte(proyecto)

        # Devolver la ruta del archivo y el tiempo de ejecución
        return jsonify(resultado)
