from flask import Flask, request
from module import account_manager


app = Flask(__name__)
app.config['DEBUG'] = False


# signup endpoint for add acount
@app.route('/signup', methods=['POST'])
def signup():
    User_manager = account_manager()
    response = User_manager.add_user(request)
    return response


# users endpoint for get or change user info
@app.route('/users/<user_id>', methods=['GET', 'PATCH'])
def getuser(user_id):
    User_manager = account_manager()
    response = User_manager.userinfo(user_id,
                                     request)
    return response


# close endpoint for delete account
@app.route('/close', methods=['POST'])
def close():
    User_manager = account_manager()
    response = User_manager.deleteaccount(request)
    return response


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
