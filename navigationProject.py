import requests
import base64
import json
import os
import time  # Importamos la librería time para hacer pausas

user_email = "pablo.munoz@bebolder.co"
token_user = "ATATT3xFfGF0UrsshZ9JZEMG-0eZQbBJ_GgT5-mSghYU8ustURw07LprkdngoC1iO8Y198B4b8nIePIekKQNhL4uQAQsVeIXhpWRY3GjtN_O-j9zOS_ZixxwZPdzcqdVsw_SKfox8okJwcj_57XIu3ZM0C7iwDFD3E-vnkLo6TQpfL-i_3mV6jM=07B92C26"


def fetch_all_boards():
    base_url = "https://bebolder.atlassian.net/rest/agile/1.0/board"
    start_at = 0
    max_results = 50
    is_last = False
    email = user_email
    api_token = token_user
    
    auth_value = base64.b64encode(f"{email}:{api_token}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth_value}",
        "Accept": "application/json"
    }

    if not os.path.exists('data'):
        os.makedirs('data')

    file_path = 'data/boards.json'

    if os.path.exists(file_path):
        os.remove(file_path)

    all_boards = [] 

    while not is_last:
        url = f"{base_url}?startAt={start_at}&maxResults={max_results}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            try:
                data = response.json()
            except json.JSONDecodeError as error:
                print("Error al procesar JSON:", error)
                return
            
            if "values" in data and len(data["values"]) > 0:
                for board in data["values"]:
                    board_data = {
                        "id": board['id'],
                        "location": {
                            "projectKey": board['location']['projectKey'] if 'location' in board and 'projectKey' in board['location'] else None,
                            "name": board['location']['name'] if 'location' in board else None
                        }
                    }
                    all_boards.append(board_data) 
            start_at += max_results
            is_last = data.get("isLast", False)

            if not is_last:
                time.sleep(2)
        else:
            print(f"Error en la petición: {response.status_code}")
            break

    all_boards_sorted = sorted(all_boards, key=lambda board: board['location']['name'] if board['location'] and board['location']['name'] else "")

    with open(file_path, 'w') as json_file:
        json.dump(all_boards_sorted, json_file, indent=4)

fetch_all_boards()
