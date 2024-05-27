import json
from flask import jsonify


class account_manager:
    '''

    '''
    def __init__(self):
        self.jsonfilepath = 'User_repository.json'

    def write_jsonfile(filepath, data):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f)

    def add_user(self, request):
        print('!!!')
        print(request)
        if request.is_json:
            data = request.get_json()
            if 'user_id' in data and 'password' in data:
                user_id = data['user_id']
                password = data['password']
                if 'nickname' not in data:
                    nickname = data['user_id']
                with open(self.jsonfilepath, 'r', encoding='utf-8') as f:
                    user_json = json.load(f)
                if user_id in user_json:
                    response = {
                        "message": "Account creation failed",
                        "cause": "already same user_id is used"
                    }
                    return jsonify(response), 400
                else:
                    user_json.update({
                        user_id: {
                            "user_id": user_id,
                            "password": password,
                            "nickname": nickname
                        }
                    })
                    self.write_jsonfile(self.jsonfilepath, user_json)
                    response = {"message": "Account successfully created",
                                "user": {
                                    "user_id": user_id,
                                    "nickname": nickname
                                }}
                    return jsonify(response), 200
        response = {"message": "Account creation failed",
                    "cause": "required user_id and password"}
        return jsonify(response), 400
