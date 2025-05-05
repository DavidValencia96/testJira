import requests
from requests.auth import HTTPBasicAuth
import time
import os
import json

user_email = "pablo.munoz@bebolder.co"
token_user = "ATATT3xFfGF0UrsshZ9JZEMG-0eZQbBJ_GgT5-mSghYU8ustURw07LprkdngoC1iO8Y198B4b8nIePIekKQNhL4uQAQsVeIXhpWRY3GjtN_O-j9zOS_ZixxwZPdzcqdVsw_SKfox8okJwcj_57XIu3ZM0C7iwDFD3E-vnkLo6TQpfL-i_3mV6jM=07B92C26"


email = user_email
api_token = token_user
jira_domain = "https://bebolder.atlassian.net"

url = f"{jira_domain}/rest/api/3/project/search"
auth = HTTPBasicAuth(email, api_token)

params = {
    'startAt': 0,  
    'maxResults': 50 
}

json_file_path = 'data/projects.json'

def obtener_proyectos():
    proyectos = []
    total_proyectos = None 

    if os.path.exists(json_file_path):
        os.remove(json_file_path)

    while True:
        response = requests.get(url, auth=auth, params=params, headers={"Accept": "application/json"})

        if response.status_code != 200:
            print(f"Error al obtener los proyectos: {response.status_code} - {response.text}")
            break
        
        data = response.json()

        if 'values' in data:
            for project in data['values']:
                project_name = project['name']
                project_key = project['key']
                if not any(p['key'] == project_key for p in proyectos):
                    proyectos.append({"name": project_name, "key": project_key})

        if total_proyectos is None:
            total_proyectos = data['total']

        if data['startAt'] + len(data['values']) >= total_proyectos:
            break

        params['startAt'] += params['maxResults']
        time.sleep(1)
    print(f"Total de proyectos obtenidos: {len(proyectos)} de {total_proyectos}")

    with open(json_file_path, 'w') as json_file:
        json.dump(proyectos, json_file, indent=4)

    return proyectos

obtener_proyectos()