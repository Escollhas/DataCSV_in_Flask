import json

from flask import Flask, request

from services import get_users, create_user, correct_data, user_login, path_user, delete_user

app = Flask(__name__)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    file_path = "./database/users.csv"
    users = get_users("./database/users.csv")
    try:
        id = int(users[-1].get("id")) + 1
    except IndexError:
        id = 1
    data = dict(id=id, **data)
    equals_mail = create_user(file_path, users, **data)
    check_error = correct_data(data)
    if equals_mail:
        return {}, 422
    elif check_error:
        return check_error
    else:
        return json.dumps(data), 201


@app.route('/login', methods=["POST"])
def login():
    users = get_users("./database/users.csv")
    data = request.get_json()
    logged = user_login(data, users)
    return logged


@app.route('/profile/<int:user_id>', methods=["PATCH", "DELETE"])
def register(user_id):
    file_path = "./database/users.csv"
    users = get_users("./database/users.csv")
    if request.method == 'PATCH':
        new_data = request.json
        if len(users) > user_id:
            output = path_user(file_path, user_id, **new_data)
            return output
        else:
            return '', 404
    if request.method == 'DELETE':
        if delete_user(user_id, file_path):
            return delete_user(user_id, file_path)


@app.route('/users')
def all_users():
    users = get_users("./database/users.csv")
    return json.dumps(users)


if __name__ == '__main__':
    app.run()
