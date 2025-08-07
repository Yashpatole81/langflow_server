import requests

url = "http://localhost:7861/run"
data = {"message": "Hello world"}

response = requests.post(url, json=data)
print(response.json())
