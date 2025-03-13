import requests
from requests.auth import HTTPBasicAuth

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

# Función para obtener los proyectos
def obtener_proyectos():
    proyectos = []

    # Realizamos la petición y obtenemos los proyectos
    while True:
        response = requests.get(url, auth=auth, params=params, headers={"Accept": "application/json"})
        
        if response.status_code != 200:
            print(f"Error al obtener los proyectos: {response.status_code} - {response.text}")
            break
        
        data = response.json()
        
        # Procesamos los proyectos obtenidos
        for project in data['values']:
            project_name = project['name']  # Nombre del proyecto
            project_key = project['key']    # Siglas del proyecto
            proyectos.append((project_name, project_key))
        
        # Si no hay más proyectos, terminamos
        if data['startAt'] + len(data['values']) >= data['total']:
            break
        
        # Si aún hay más proyectos, ajustamos el offset
        params['startAt'] += params['maxResults']

    print(proyectos)  # Agregar esta línea para verificar los proyectos
    return proyectos
