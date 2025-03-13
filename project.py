import requests
from requests.auth import HTTPBasicAuth
import time
import os
import json

# Datos de autenticación y configuración
email = "pablo.munoz@bebolder.co"
api_token = "ATATT3xFfGF0UrsshZ9JZEMG-0eZQbBJ_GgT5-mSghYU8ustURw07LprkdngoC1iO8Y198B4b8nIePIekKQNhL4uQAQsVeIXhpWRY3GjtN_O-j9zOS_ZixxwZPdzcqdVsw_SKfox8okJwcj_57XIu3ZM0C7iwDFD3E-vnkLo6TQpfL-i_3mV6jM=07B92C26"
jira_domain = "https://bebolder.atlassian.net"

# URL para la API de proyectos
url = f"{jira_domain}/rest/api/3/project/search"

# Configuración de autenticación
auth = HTTPBasicAuth(email, api_token)

# Parámetros de la solicitud (paginación)
params = {
    'startAt': 0,  # Primer proyecto
    'maxResults': 50  # Número de proyectos por llamada
}

# Ruta del archivo JSON donde se almacenarán los proyectos
json_file_path = 'data/projects.json'

# Función para obtener los proyectos
def obtener_proyectos():
    proyectos = []
    total_proyectos = None 

    # Siempre eliminamos el archivo JSON anterior para obtener proyectos actualizados
    if os.path.exists(json_file_path):
        os.remove(json_file_path)

    while True:
        response = requests.get(url, auth=auth, params=params, headers={"Accept": "application/json"})
        
        # Comprobar el estado de la respuesta
        if response.status_code != 200:
            print(f"Error al obtener los proyectos: {response.status_code} - {response.text}")
            break
        
        data = response.json()

        # Verificamos si la respuesta contiene proyectos
        if 'values' in data:
            for project in data['values']:
                project_name = project['name']  # Nombre del proyecto
                project_key = project['key']    # Siglas del proyecto
                # Verificamos si el proyecto ya está en la lista antes de agregarlo
                if not any(p['key'] == project_key for p in proyectos):
                    proyectos.append({"name": project_name, "key": project_key})

        # Verificamos si es la primera vez que obtenemos el total
        if total_proyectos is None:
            total_proyectos = data['total']
        
        # Verificamos si hemos obtenido todos los proyectos
        if data['startAt'] + len(data['values']) >= total_proyectos:
            break  # Si hemos llegado al final, salir del bucle
        
        # Aumentamos el valor de 'startAt' para la siguiente página
        params['startAt'] += params['maxResults']
        
        # Pausa de 1 segundo entre solicitudes
        time.sleep(1)
        

    print(f"Total de proyectos obtenidos: {len(proyectos)} de {total_proyectos}")
    
    # Guardamos los proyectos en un archivo JSON
    with open(json_file_path, 'w') as json_file:
        json.dump(proyectos, json_file, indent=4)

    return proyectos  # Retornar los proyectos para usarlos directamente


# Llamar a la función para obtener los proyectos
obtener_proyectos()
