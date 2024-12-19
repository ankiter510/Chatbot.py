import requests

url = "http://127.0.0.1:5000/chat"
data = {"query": "What is the return policy?"}

response = requests.post(url, json=data)
print(response.json())