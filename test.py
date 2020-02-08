import requests

r = requests.get("https://coronavirus.m.pipedream.net/")
data = r.json()
print(data)