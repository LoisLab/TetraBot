import requests

URL = "http://loislabpi-14.local/action="
botcommand = 80

r = requests.get(URL+str(botcommand))
print(r)


