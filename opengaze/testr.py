import requests 
import json

req = requests.get(url="http://127.0.0.1:8000/get-gaze")

reqjson = json.loads(req.json())
# while True :
print(reqjson["frame"])