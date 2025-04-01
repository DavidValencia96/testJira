import requests
import json
from flask import jsonify, current_app
from base64 import b64encode
import os
import time
from datetime import datetime
import csv
from requests.auth import HTTPBasicAuth

def obtener_sprints_jira(proyecto_id):
    url = f"https://bebolder.atlassian.net/rest/greenhopper/1.0/sprintquery/{proyecto_id}?includeFutureSprints=false&_=1743513788133"

    EMAIL = "pablo.munoz@bebolder.co"
    API_TOKEN = "ATATT3xFfGF0UrsshZ9JZEMG-0eZQbBJ_GgT5-mSghYU8ustURw07LprkdngoC1iO8Y198B4b8nIePIekKQNhL4uQAQsVeIXhpWRY3GjtN_O-j9zOS_ZixxwZPdzcqdVsw_SKfox8okJwcj_57XIu3ZM0C7iwDFD3E-vnkLo6TQpfL-i_3mV6jM=07B92C26"

    auth = HTTPBasicAuth(EMAIL, API_TOKEN)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)

    data_folder = os.path.join(current_app.root_path, 'data')
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    json_data_sprint = os.path.join(data_folder, 'data_sprint.json')

    if os.path.exists(json_data_sprint):
        os.remove(json_data_sprint)

    if response.status_code == 200:
        json_response = response.json()
        if "sprints" in json_response:
            sprints = json_response["sprints"]
            sprint_data = []
            for sprint in sprints:
                sprint_data.append({
                    "id": sprint["id"],
                    "name": sprint["name"],
                    "state": sprint["state"],
                    "goal": sprint.get("goal", ""),
                    "sprintVersion": sprint["sprintVersion"]
                })
            with open(json_data_sprint, 'w', encoding='utf-8') as json_file:
                json.dump(sprint_data, json_file, ensure_ascii=False, indent=4)
            return sprint_data 
        else:
            raise Exception("No se encontraron sprints.")
    else:
        raise Exception(f"Error al obtener datos de Jira: {response.status_code}")

def obtener_hus_de_sprint(proyecto_id, sprint_id):
    start_time = time.time() 
    EMAIL = "pablo.munoz@bebolder.co"
    API_TOKEN = "ATATT3xFfGF0UrsshZ9JZEMG-0eZQbBJ_GgT5-mSghYU8ustURw07LprkdngoC1iO8Y198B4b8nIePIekKQNhL4uQAQsVeIXhpWRY3GjtN_O-j9zOS_ZixxwZPdzcqdVsw_SKfox8okJwcj_57XIu3ZM0C7iwDFD3E-vnkLo6TQpfL-i_3mV6jM=07B92C26"
    PROYECTO_ID = proyecto_id
    SPRINT_ID = sprint_id

    url = f"https://bebolder.atlassian.net/rest/greenhopper/1.0/rapid/charts/sprintreport?rapidViewId={PROYECTO_ID}&sprintId={SPRINT_ID}&_=1743432986996"
    auth_value = b64encode(f"{EMAIL}:{API_TOKEN}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_value}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 403:
        return {"error": "🚨 Error 403: No tienes acceso a la API de Jira. Revisa tu correo, token o permisos."}, 403
    elif response.status_code != 200:
        return {"error": f"🚨 Error en la petición: Código {response.status_code}", "details": response.text}, response.status_code

    data = response.json()

    json_file_path = f'data/issues_sprint_{proyecto_id}_{sprint_id}.json'

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    rows = [] 

    added_during_sprint = data["contents"].get("issueKeysAddedDuringSprint", {})

    for issue in data["contents"].get("completedIssues", []):
        if issue.get("typeName") in ["Historia", "Error"]:
            added_during_sprint_value = added_during_sprint.get(issue.get("key"), False)
            updated_at = datetime.utcfromtimestamp(issue.get("updatedAt", 0) / 1000).strftime('%Y-%m-%d %H:%M:%S')  # Convertir timestamp
            rows.append([ 
                issue.get("key"),
                issue.get("typeName"),
                issue.get("summary"),
                issue.get("priorityName"),
                issue.get("assigneeName"),
                issue.get("statusName"),
                issue.get("projectId"),
                updated_at,
                "Issue completado en el sprint actual", 
                added_during_sprint_value 
            ])

    for issue in data["contents"].get("issuesNotCompletedInCurrentSprint", []):
        if issue.get("typeName") in ["Historia", "Error"]:
            added_during_sprint_value = added_during_sprint.get(issue.get("key"), False)
            updated_at = datetime.utcfromtimestamp(issue.get("updatedAt", 0) / 1000).strftime('%Y-%m-%d %H:%M:%S')
            rows.append([
                issue.get("key"),
                issue.get("typeName"),
                issue.get("summary"),
                issue.get("priorityName"),
                issue.get("assigneeName"),
                issue.get("statusName"),
                issue.get("projectId"),
                updated_at,
                "Issue NO completado en el sprint actual",
                added_during_sprint_value 
            ])

    for issue in data["contents"].get("puntedIssues", []):
        if issue.get("typeName") in ["Historia", "Error"]:
            added_during_sprint_value = added_during_sprint.get(issue.get("key"), False)
            updated_at = datetime.utcfromtimestamp(issue.get("updatedAt", 0) / 1000).strftime('%Y-%m-%d %H:%M:%S')
            rows.append([
                issue.get("key"),
                issue.get("typeName"),
                issue.get("summary"),
                issue.get("priorityName"),
                issue.get("assigneeName"),
                issue.get("statusName"),
                issue.get("projectId"),
                updated_at,
                "Issue postergado",
                added_during_sprint_value 
            ])

    file_path = f'data/issues_sprint_{proyecto_id}_{sprint_id}.csv'

    if rows:
        with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([ 
                "key", "Tipo issue", "Titulo", "Prioridad", "Assignado", 
                "Estado", "ID Proyecto", "Actualizada", "Categoria", "Añadido durante el sprint"
            ])
            csv_writer.writerows(rows)

    if not os.path.exists('data'):
        os.makedirs('data')

    end_time = time.time()
    execution_time = end_time - start_time  

    return {"archivo": f"https://testjira.onrender.com/{file_path}", "tiempo": execution_time}
