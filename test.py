import requests
from bs4 import BeautifulSoup
import json

session = requests.session()

response = session.get('https://fr.getaround.com/login')

soup = BeautifulSoup(response.text)

token = soup.find("input", {"name" : "authenticity_token"}).attrs['value']

data = {"authenticity_token" : token,
        "commit":"Se connecter",
        "user[email]": 'anatolecallies@gmail.com',
        "user[password]": 'zVQ2CTCJ',
        "user[remember_me]": 1}

session.post('https://fr.getaround.com/login', data=data)

soup = BeautifulSoup(json.loads(session.get('https://fr.getaround.com/dashboard/cars/326693/open_management/status').text)['html'])

print(soup.find("a", {"target" : "_blank"}).attrs['href'])
