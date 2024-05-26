import json
import os
import msvcrt
import time

jsonfilepath = 'User_repository.json'

def write_jsonfile(filepath, data):
    # Avoid potential PermissionError
    while True:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                msvcrt.locking(f.fileno(),
                               msvcrt.LK_NBLCK,
                               os.path.getsize(filepath)+1)
                json.dump(data, f)
                break
        except PermissionError:
            time.sleep(0.1)


class user_repository:
    '''
    
    '''
    def __init__(self) -> None:
        with open(jsonfilepath, 'r', encoding='utf-8') as f:
            self.user_json = json.load(f)
        self.response = {}
    

    def add_user(self, data):
        pass
