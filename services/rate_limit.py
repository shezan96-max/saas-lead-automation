import time

last_request_time = {}

def check_rate_limit(client_name : str):
    now = time.time()

    if client_name in last_request_time:
        if now - last_request_time[client_name] < 5:
            return False
        
    last_request_time[client_name] = now
    return True
