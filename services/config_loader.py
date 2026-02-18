import json
import os

def load_client_config(client_name : str):
    path = f"clients/{client_name}/config.json"

    if not os.path.exists(path):
        return {}
    with open(path,"r") as f:
        return json.load(f)
    
    