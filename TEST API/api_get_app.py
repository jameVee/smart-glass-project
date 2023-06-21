import requests
api_url = "http://127.0.0.1:5000/api_get_data"
response = requests.get(api_url)

print(response.status_code)
print(response.json())
print(response.headers)