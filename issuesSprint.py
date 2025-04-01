import requests
import json
from flask import jsonify
from base64 import b64encode
import os
import csv

def obtener_hus_de_sprint(proyecto_id, sprint_id):
    EMAIL = "laura.posada@bebolder.co"
    API_TOKEN = "ATATT3xFfGF0UrsshZ9JZEMG-0eZQbBJ_GgT5-mSghYU8ustURw07LprkdngoC1iO8Y198B4b8nIePIekKQNhL4uQAQsVeIXhpWRY3GjtN_O-j9zOS_ZixxwZPdzcqdVsw_SKfox8okJwcj_57XIu3ZM0C7iwDFD3E-vnkLo6TQpfL-i_3mV6jM=07B92C26";  
    PROYECTO_ID = proyecto_id
    SPRINT_ID = sprint_id

    # Construir la URL para hacer la solicitud
    url = f"https://bebolder.atlassian.net/rest/greenhopper/1.0/rapid/charts/sprintreport?rapidViewId={PROYECTO_ID}&sprintId={SPRINT_ID}&_=1743432986996"

    # Crear el encabezado de autorización base64
    auth_value = b64encode(f"{EMAIL}:{API_TOKEN}".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_value}",
        "Accept": "application/json"
    }

    # Realizar la solicitud HTTP GET a la API de Jira
    response = requests.get(url, headers=headers)

    # Verificar el estado de la respuesta
    if response.status_code == 403:
        return {"error": "🚨 Error 403: No tienes acceso a la API de Jira. Revisa tu correo, token o permisos."}, 403
    elif response.status_code != 200:
        return {"error": f"🚨 Error en la petición: Código {response.status_code}", "details": response.text}, response.status_code

    # Procesar los datos JSON de la respuesta
    data = response.json()
    
        # Definir el nombre del archivo JSON
    json_file_path = 'data/issues_sprint_response.json'

    # Guardar la respuesta completa en un archivo JSON
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    # Comenzamos a extraer los datos necesarios
    rows = []  # Almacenamos las filas del CSV

    # Datos de issueKeysAddedDuringSprint
    added_during_sprint = data["contents"].get("issueKeysAddedDuringSprint", {})
    
    # Datos de completedIssues
    if "completedIssues" in data["contents"]:
        for issue in data["contents"]["completedIssues"]:
            # Filtramos solo Story o Bug
            if issue.get("typeName") in ["Story", "Bug"]:
                # Verificamos si la key está en 'added_during_sprint'
                added_during_sprint_value = added_during_sprint.get(issue.get("key"), False)
                rows.append([
                    issue.get("key"),
                    issue.get("typeName"),
                    issue.get("summary"),
                    issue.get("priorityName"),
                    issue.get("done"),
                    issue.get("assigneeName"),
                    issue.get("statusName"),
                    issue.get("projectId"),
                    issue.get("updatedAt"),
                    "completedIssues",  # Columna para identificar el tipo de issue
                    added_during_sprint_value  # Aquí se marca 'True' o 'False' dependiendo de si la key está en 'issueKeysAddedDuringSprint'
                ])

    # Datos de issuesNotCompletedInCurrentSprint
    if "issuesNotCompletedInCurrentSprint" in data["contents"]:
        for issue in data["contents"]["issuesNotCompletedInCurrentSprint"]:
            # Filtramos solo Story o Bug
            if issue.get("typeName") in ["Story", "Bug"]:
                # Verificamos si la key está en 'added_during_sprint'
                added_during_sprint_value = added_during_sprint.get(issue.get("key"), False)
                rows.append([
                    issue.get("key"),
                    issue.get("typeName"),
                    issue.get("summary"),
                    issue.get("priorityName"),
                    issue.get("done"),
                    issue.get("assigneeName"),
                    issue.get("statusName"),
                    issue.get("projectId"),
                    issue.get("updatedAt"),
                    "issuesNotCompletedInCurrentSprint",
                    added_during_sprint_value  # Aquí se marca 'True' o 'False' dependiendo de si la key está en 'issueKeysAddedDuringSprint'
                ])

    # Datos de puntedIssues
    if "puntedIssues" in data["contents"]:
        for issue in data["contents"]["puntedIssues"]:
            # Filtramos solo Story o Bug
            if issue.get("typeName") in ["Story", "Bug"]:
                # Verificamos si la key está en 'added_during_sprint'
                added_during_sprint_value = added_during_sprint.get(issue.get("key"), False)
                rows.append([
                    issue.get("key"),
                    issue.get("typeName"),
                    issue.get("summary"),
                    issue.get("priorityName"),
                    issue.get("done"),
                    issue.get("assigneeName"),
                    issue.get("statusName"),
                    issue.get("projectId"),
                    issue.get("updatedAt"),
                    "puntedIssues",
                    added_during_sprint_value  # Aquí se marca 'True' o 'False' dependiendo de si la key está en 'issueKeysAddedDuringSprint'
                ])

    # Definir el nombre del archivo CSV
    file_path = 'data/issues_sprint.csv'

        
    # Verificar si el directorio existe, si no, lo creamos
    if not os.path.exists('data'):
        os.makedirs('data')

    

    # Escribir los datos en el archivo CSV
    with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Escribir el encabezado
        csv_writer.writerow([
            "key", "typeName", "summary", "priorityName", "done", "assigneeName", 
            "statusName", "projectId", "updatedAt", "Category", "AddedDuringSprint"
        ])
        # Escribir las filas de los issues
        csv_writer.writerows(rows)

    # Retorno del archivo CSV y JSON
    return {
        "message": "✅ Issues guardadas exitosamente en 'issues_sprint.csv' y 'issues_sprint_response.json'.",
        "file": file_path,
        "json_file": json_file_path
    }
