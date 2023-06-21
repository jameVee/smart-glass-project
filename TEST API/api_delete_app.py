import requests
import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
file = open(dir_path+"\data_post_del.json")
data = json.load(file)

api_url = "http://172.20.10.3:5000/api_delete_data/"

r = requests.post(api_url, json=data)

print('SQL Command : ', r.text)

print(f"Status Code: {r.status_code}")