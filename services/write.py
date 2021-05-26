import csv
import json

import numpy as np
import pandas as pd
from flask import jsonify


def equals_mail(all_users, email):
    same_email = [i for i in all_users if email == i["email"]]
    if same_email:
        return True
    else:
        return False


def create_user(file, all_users, **user):
    FIELDNAMES = [
        "id",
        "name",
        "email",
        "password",
        "age"]
    if not equals_mail(all_users, user.get("email")):
        all_users.append(user)
        with open(file, mode="w") as f:
            user = csv.DictWriter(f, fieldnames=FIELDNAMES)
            user.writeheader()
            user.writerows(all_users)
        return False
    else:
        return True


def correct_data(new_user):
    if not isinstance(new_user.get("name", "email"), str) \
            and isinstance(new_user.get("age"), int):
        return jsonify({
            "status": "error",
            "message": [
                "name is required and string",
                "email is required and string",
                "password is required and any type",
                "age is required and is int"
            ]
        })


def user_login(user_data, all_users):
    user_data = [i for i in all_users if user_data["email"] == i["email"]
                 and user_data["password"] == i["password"]]
    if user_data:
        del user_data[0]['password']
        return json.dumps(user_data[0]), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Incorrect email / password combination"
        }), 401


def path_user(file_path, user_id, **new_data):
    df = pd.read_csv(file_path)
    df.loc[df["id"] == user_id - 1]
    if new_data.get("name"):
        df.loc[df.index[user_id - 1], "name"] = new_data["name"]
    if new_data.get("email"):
        df.loc[df.index[user_id - 1], "email"] = new_data["email"]
    if new_data.get("password"):
        df.loc[df.index[user_id - 1], "password"] = new_data["password"]
    if new_data.get("age"):
        df.loc[df.index[user_id - 1], "age"] = new_data["age"]
    refresh_csv(file_path, df)
    output = df.iloc[user_id - 1].to_dict()
    output.pop('password')
    return json.dumps(output, cls=NpEncoder)


def refresh_csv(file_path, data):
    return pd.DataFrame(data).to_csv(file_path, header=True, index=False)


# Solution for TypeError: Object of type int64 is not JSON serializable
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


def delete_user(user_id, file_path):
    df = pd.read_csv(file_path)
    df.drop(df.index[(df["id"] == user_id)], axis=0, inplace=True)
    refresh_csv(file_path, df)
    return '', 204
