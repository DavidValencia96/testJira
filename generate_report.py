import requests
import base64
import time
import os
import csv
import json
import unicodedata
from datetime import datetime
from flask import jsonify, request, send_from_directory

user_email = "pablo.munoz@bebolder.co"
token_user = "ATATT3xFfGF0UrsshZ9JZEMG-0eZQbBJ_GgT5-mSghYU8ustURw07LprkdngoC1iO8Y198B4b8nIePIekKQNhL4uQAQsVeIXhpWRY3GjtN_O-j9zOS_ZixxwZPdzcqdVsw_SKfox8okJwcj_57XIu3ZM0C7iwDFD3E-vnkLo6TQpfL-i_3mV6jM=07B92C26"
domain = "https://bebolder.atlassian.net"

def generar_reporte(proyecto, issue_types=None):
    email = user_email
    api_token = token_user

    auth_string = f"{email}:{api_token}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()

    start_at = 0
    max_results = 100
    total = 0

    jql_query = f"project={proyecto}"
    if issue_types:
        issue_types_query = ', '.join([f'"{issue_type}"' for issue_type in issue_types]) 
        jql_query += f" AND type IN ({issue_types_query})"

    
    archivo_csv = f"data/issues_{proyecto}.csv"
    if os.path.exists(archivo_csv):
        os.remove(archivo_csv)
        
    
    def obtener_issues_jira():
        nonlocal start_at, total
        while start_at < total or total == 0:
            url = f"{domain}/rest/api/3/search?jql={jql_query}&startAt={start_at}&maxResults={max_results}"
            headers = {
                "Authorization": f"Basic {encoded_auth}",
                "Accept": "application/json"
            }

            try:
                response = requests.get(url, headers=headers, timeout=130)
                response.raise_for_status()
                json_response = response.json()
                total = json_response['total']
                
                with open(f"data/issues_{proyecto}.json", "a") as json_file:
                    json.dump(json_response, json_file, indent=4)
                
                with open(f"data/issues_{proyecto}.csv", mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)

                    if start_at == 0:
                        writer.writerow(["Proyecto", "Clave/ID", "Tipo issue", "Prioridad", "Informador", "Creada", "Titulo", "Estado", "Responsable", "Actualizada", "Cantidad de sprint",  "Sprint actual", "Fechas de sprint", "Nombres Sprint", "Definición de hecho", "Puntos de historia", "Puntos estimados", "Puntos ejecutados", "Sumatoria tiempo empleado", "Seguimiento de tiempo HH/MM", "Codigo externo"])

                    for issue in json_response['issues']:
                        project = issue['fields']['project']['name']

                        key = issue['key']

                        issuetype = issue['fields']['issuetype'].get('name', None) 
                        if not issuetype: 
                            issuetype = "N/A"

                        priority = issue['fields']['priority'].get('name', None) 
                        if not priority: 
                            priority = "N/A"

                        reporter = issue['fields']['reporter'].get('displayName', None) 
                        if not reporter: 
                            reporter = "N/A"
                        created = issue['fields']['created']
                        created_datetime = datetime.strptime(created, "%Y-%m-%dT%H:%M:%S.%f%z")
                        created_date = created_datetime.date()
                        summary = issue['fields']['summary']
                        status = issue['fields']['status']['name']
                        assignee_name = issue['fields'].get('assignee', None)
                        if assignee_name:
                            assignee_name = assignee_name.get('displayName', 'No asignado')
                        else:
                            assignee_name = "No asignado"
                        updated = issue['fields']['updated']
                        try:
                            updated_datetime = datetime.strptime(updated, "%Y-%m-%dT%H:%M:%S.%f%z")
                            updated_date = updated_datetime.strftime("%Y-%m-%d")
                        except ValueError as e:
                            updated_date = "Sin actualizar"
                            
                        amountSprint = issue['fields'].get('customfield_10020', None) 
                        if amountSprint is None or len(amountSprint) == 0:
                            amountSprint = "Sin sprint"
                        else:
                            amountSprint = f"{len(amountSprint)} Sprints"

                        currentSprint = issue['fields'].get('customfield_10020', None)
                        if currentSprint:
                            SpritnCurrent = next((sprint.get("name", "N/A") for sprint in currentSprint if sprint.get("state") == "active"), "N/A")
                        else:
                            SpritnCurrent = "N/A"

                        dateSprint = issue['fields'].get('customfield_10020', None)
                        if dateSprint is not None:
                            filtered_sprints = []
                            for sprint in dateSprint:
                                start_date = sprint.get("startDate")
                                if start_date:
                                    start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
                                filtered_sprints.append({
                                    "InicioSprint": start_date,
                                })
                        else:
                            filtered_sprints = 'N/A'

                        NameSprint = issue['fields'].get('customfield_10020', None)

                        if NameSprint is not None:
                            filtered_name_sprints = []
                            for sprint in NameSprint:
                                name_sprint = sprint.get("name") 
                                filtered_name_sprints.append(name_sprint)
                        else:
                            filtered_name_sprints = 'N/A'

                        definitionOfFact = issue['fields'].get('customfield_10048', None)
                        if isinstance(definitionOfFact, dict) and 'value' in definitionOfFact:
                            definitionOfFact = definitionOfFact['value']
                        else:
                            definitionOfFact = "N/A"
                        storyPoint = issue['fields'].get('customfield_10033', None) 
                        if not storyPoint: 
                            storyPoint = "0.0"
                        storyPointEstimated = issue['fields'].get('customfield_10016', None) 
                        if not storyPointEstimated: 
                            storyPointEstimated = "0.0"
                        storyPointExecuted = issue['fields'].get('customfield_10046', None) 
                        if not storyPointExecuted: 
                            storyPointExecuted = "0.0"
                        aggregatetimespent = issue['fields'].get('aggregatetimespent', None) 
                        if not aggregatetimespent: 
                            aggregatetimespent = "0.0"
                        timeTracking = issue['fields'].get('aggregatetimespent', None) 
                        if not timeTracking: 
                            timeTracking = "0H 0M"
                        else: 
                            hours = timeTracking // 3600
                            minutes = (timeTracking % 3600) // 60
                            timeTracking = F"{hours}H {minutes}M"
                        externalCode = issue['fields'].get('customfield_10057', None) 
                        if not externalCode: 
                            externalCode = "N/A"

                        writer.writerow([project, key, issuetype, priority, reporter, created_date, summary, status, assignee_name, updated_date, amountSprint, SpritnCurrent, filtered_sprints, filtered_name_sprints, definitionOfFact, storyPoint, storyPointEstimated, storyPointExecuted, aggregatetimespent, timeTracking, externalCode])
                start_at += max_results
            except requests.exceptions.RequestException as e:
                return jsonify({"error": f"Error en la extracción de datos: {e}"}), 500

    start_time = time.time()
    obtener_issues_jira()
    end_time = time.time()
    execution_time = end_time - start_time
    return {"archivo": f"https://testjira.onrender.com/data/issues_{proyecto}.csv", "tiempo": execution_time}

def generar_reporte_route(app):
    @app.route('/generar_reporte', methods=['POST'])
    def reporte_route():
        data = request.get_json()
        proyecto = data['proyecto']
        issue_types = data.get('issueTypes', [])  
        resultado = generar_reporte(proyecto, issue_types)
        return jsonify(resultado)

    @app.route('/data/<path:filename>')
    def serve_file(filename):
        return send_from_directory(os.path.join(app.root_path, 'data'), filename, as_attachment=False)
