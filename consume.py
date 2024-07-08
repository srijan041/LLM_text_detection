import requests

str = str(input("Enter text: "))
obj = {'text': str}

url = 'http://127.0.0.1:8000/ai/'

x = requests.post(url, json=obj)
print(x.text)