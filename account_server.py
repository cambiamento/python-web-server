from flask import Flask, request
from module import account_manager


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
    User_manager = account_manager()
    response = User_manager.userinfo(user_id,
                                     auth_header,
                                     request.method)
    return response


@app.route('/close', methods=['POST'])
def close():
    auth_header = request.headers.get('Authorization')
    User_manager = account_manager()
    response = User_manager.deleteaccount(auth_header)
    return response


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
