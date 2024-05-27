import json
from flask import jsonify
import base64


class account_manager:
    '''
    The class for account management
    method:
    write_jsonfile: overwrite json file
    Authorization: get userid and password from encoded info
    add_user: add new account in json file
    userinfo: get or change account info from json file
    deleteaccount: delete account from json file
    '''
    def __init__(self):
        self.jsonfilepath = 'User_repository.json'

    def write_jsonfile(self, filepath, data):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f)

    def Authorization(self, auth_header):
        auth_token = auth_header.split(' ')[1]
        auth_decoded = base64.b64decode(auth_token).decode('utf-8')
        input_userid, input_password = auth_decoded.split(':')
        return input_userid, input_password

    def add_user(self, request):
        if request.is_json:
            data = request.get_json()
            # Check the existence of user_id and password
            if 'user_id' in data and 'password' in data:
                user_id = data['user_id']
                password = data['password']
                # set userid as nickname if nickname is empty
                if 'nickname' not in data:
                    nickname = data['user_id']
                with open(self.jsonfilepath, 'r', encoding='utf-8') as f:
                    user_json = json.load(f)
                # userid already existed
                if user_id in user_json:
                    response = {
                        "message": "Account creation failed",
                        "cause": "already same user_id is used"
                    }
                    return jsonify(response), 400
                # update user_repository.json
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

    def userinfo(self, user_id, request):
        method = request.method
        auth_header = request.headers.get('Authorization')
        with open(self.jsonfilepath, 'r', encoding='utf-8') as f:
            user_json = json.load(f)
        # get authorization info from encoded string
        try:
            input_userid, input_password = self.Authorization(auth_header)
        except Exception:
            response = {"message": "Authentication Failed"}
            return jsonify(response), 401
        # No user exist
        if user_id not in user_json:
            response = {"message": "No User found"}
            return jsonify(response), 404
        else:
            # authorization passed
            if input_password == user_json[input_userid]["password"]:
                if method == 'GET':
                    response = {"message": "User details by user_id",
                                "user": user_json[user_id]}
                    return jsonify(response), 200
                else:
                    # get request body as dict
                    data = request.get_json()
                    # failed when no nickname and comment
                    if all(['nickname' not in data,
                            'comment' not in data]):
                        response = {"message": "User updation failed",
                                    "cause": "required nickname or comment"}
                        return jsonify(response), 400
                    # failed when update target is userid or password
                    elif any(['user_id' in data,
                              'password' in data]):
                        response = {"message": "User updation failed",
                                    "cause": "not updatable user_id and password"}
                    # failed when userinfo is different from authorized one
                    elif input_userid != user_id:
                        response = {"message": "No Permission for Update"}
                        return jsonify(response), 403
                    else:
                        for k, v in data.items():
                            user_json[user_id][k] = v
                        response = {"message": "User successfully updated",
                                    "recipe": [data]}
                        return jsonify(response), 200
            else:
                response = {"message": "Authentication Failed"}
                return jsonify(response), 401

    def deleteaccount(self, request):
        auth_header = request.headers.get('Authorization')
        with open(self.jsonfilepath, 'r', encoding='utf-8') as f:
            user_json = json.load(f)
        try:
            input_userid, input_password = self.Authorization(auth_header)
        except Exception:
            response = {"message": "Authentication Failed"}
            return jsonify(response), 401

        # Authorization passed
        if all([input_userid in user_json,
                input_password == user_json[input_userid]["password"]]):
            user_json.pop(input_userid)
            self.write_jsonfile(self.jsonfilepath, user_json)
            response = {"message": "Account and user successfully removed"}
            return jsonify(response), 200
        else:
            response = {"message": "Authentication Failed"}
            return jsonify(response), 401
