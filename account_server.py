from flask import Flask, request
from module import account_manager


app = Flask(__name__)


# @app.route('/', methods=['GET'])
# def root():
#     return 'OK'


@app.route('/signup', methods=['POST'])
def signup():
    User_manager = account_manager()
    response = User_manager.add_user(request)
    return response


@app.route('/users/<user_id>', methods=['GET', 'PATCH'])
def getuser():
    print(request)
    return 'OK'


@app.route('/close', methods=['GET'])
def close():
    print(request)
    return 'OK'


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
