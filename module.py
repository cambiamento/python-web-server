import json
from flask import jsonify
import base64


class account_manager:
    '''

    '''
    def __init__(self):
        self.jsonfilepath = 'User_repository.json'

    def write_jsonfile(self, filepath, data):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f)

    def add_user(self, request):
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

    def userinfo(self, user_id, auth_header, method):
        with open(self.jsonfilepath, 'r', encoding='utf-8') as f:
            user_json = json.load(f)
        try:
            auth_token = auth_header.split(' ')[1]
            auth_decoded = base64.b64decode(auth_token).decode('utf-8')
            input_userid, input_password = auth_decoded.split(':')
        except Exception:
            response = {"message": "Authentication Failed"}
            return jsonify(response), 401

        if user_id not in user_json:
            response = {"message": "No User found"}
            return jsonify(response), 404
        else:
            if input_password == user_json[input_userid]["password"]:
                if method == 'GET':
                    response = {"message": "User details by user_id",
                                "user": user_json[user_id]}
                    return jsonify(response), 200
                else:
                    if all(['nickname' not in user_json[user_id],
                            'comment' not in user_json[user_id]]):
                        response = {"message": "User updation failed",
                                    "cause": "required nickname or comment"}
                        return jsonify(response), 400
                    elif any(['user_id' in user_json[user_id],
                              'password' in user_json[user_id]]):
                        response = {"message": "User updation failed",
                                    "cause": "not updatable user_id and password"}
                    elif input_userid != user_id:
                        response = {"message": "No permission for update"}
                        return jsonify(response), 403
            else:
                response = {"message": "Authentication Failed"}
                return jsonify(response), 401

    def deleteaccount(self, auth_header):
        with open(self.jsonfilepath, 'r', encoding='utf-8') as f:
            user_json = json.load(f)
        try:
            auth_token = auth_header.split(' ')[1]
            auth_decoded = base64.b64decode(auth_token).decode('utf-8')
            input_userid, input_password = auth_decoded.split(':')
        except Exception:
            response = {"message": "Authentication Failed"}
            return jsonify(response), 401

        if all([input_userid in user_json,
                input_password == user_json[input_userid]["password"]]):
            user_json.pop(input_userid)
            self.write_jsonfile(self.jsonfilepath, user_json)
            response = {"message": "Account and user successfully removed"}
            return jsonify(response), 200
        else:
            response = {"message": "Authentication Failed"}
            return jsonify(response), 401
