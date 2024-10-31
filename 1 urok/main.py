import requests

url_template ="https://wttr.in/{}"
payload = {
    "lang": "ru",
    "M": "",
    "n": "",
    "q": "",
    "T": ""
}

places = "London", "SVO", "Череповец"
for place in places:
    response = requests.get(url_template.format(place), params=payload)
    response.raise_for_status()
    print(response.text)
