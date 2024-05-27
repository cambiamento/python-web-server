from flask import Flask, request
from module import account_manager
import base64


app = Flask(__name__)
app.config['DEBUG'] = False


@app.route('/signup', methods=['POST'])
def signup():
    User_manager = account_manager()
    response = User_manager.add_user(request)
    return response


@app.route('/users/<user_id>', methods=['GET', 'PATCH'])
def getuser(user_id):
    auth_header = request.headers.get('Authorization')
    auth_token = auth_header.split(' ')[1]
    auth_decoded = base64.b64decode(auth_token).decode('utf-8')
    input_userid, input_password = auth_decoded.split(':')
    print('!!!')
    print(input_userid)
    print(input_password)
    print('!!!')
    User_manager = account_manager()
    response = User_manager.userinfo(user_id,
                                     auth_header,
                                     request.method)
    return response


@app.route('/close', methods=['GET'])
def close():
    print(request)
    return 'OK'


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
