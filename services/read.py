import os
import pandas
import pandas as pd


def get_users(file_path):
    if not os.path.exists(file_path):
        pd.DataFrame(columns=['id', 'name', 'email', 'password', 'age']).to_csv(file_path, header=True, index=False)
        return "Base de dados criado com sucesso"
    if os.path.exists(file_path):
        return pandas.read_csv(file_path).to_dict('records')

