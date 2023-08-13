import requests

url = "https://api.distancematrix.ai/maps/api/distancematrix/json"

querystring = {
    "origins": "Tehran",
    "destinations": "Mashhad",
    "key": "yPDWO6I8nEKDcAvC2OFapG6m2ygMk"}

response = requests.get(url, params=querystring, proxies={"https": "127.0.0.1:5556"})

print(response.json())
