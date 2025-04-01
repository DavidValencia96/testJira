import requests
import json
from flask import jsonify
from base64 import b64encode
import os
import time
from datetime import datetime
import csv

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

    file_path = f'data/issues_sprint_{proyecto_id}_{sprint_id}.csv'
    
    if not os.path.exists('data'):
        os.makedirs('data')

    with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([
            "key", "typeName", "summary", "priorityName", "done", "assigneeName", 
            "statusName", "projectId", "updatedAt", "Category", "AddedDuringSprint"
        ])
        csv_writer.writerows(rows)

    end_time = time.time()
    execution_time = end_time - start_time  

    return {"archivo": f"https://testjira.onrender.com/{file_path}", "tiempo": execution_time}
