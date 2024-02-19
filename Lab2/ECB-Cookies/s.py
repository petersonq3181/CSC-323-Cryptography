import requests

url = 'http://0.0.0.0:8080/'


# register user 0
data = {
    'user': 'a', 
    'password': '12' 
}

requests.get(url + 'register')
response = requests.post(url + 'register', data=data)

if response.ok:
    print("registration successful")
    print(response.text)
else:
    print("registration failed")

# login as user 0 
data = {
    'user': 'a', 
    'password': '12' 
}

requests.get(url)
response = requests.post(url, data=data)

gg = requests.get(url + 'home')
if gg.ok:
    print('gg')
    print(gg.text)
else:
    print('fuck')

if response.ok:
    print("login successful")
    print(response.text)
else:
    print("login failed")


# 3c7d0cbb889f9ba0400f8dafbb5fd18465900ec69c7b92caa8e41e7f347d703e