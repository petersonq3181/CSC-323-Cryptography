import requests

# Create a session object
session = requests.Session()

url = 'http://0.0.0.0:8080/'

# Register a user
reg_data = {
    'user': 'a',
    'password': '12'
}
session.get(url + 'register')  # Initial GET might be necessary for CSRF token, etc.
reg_response = session.post(url + 'register', data=reg_data)

if reg_response.ok:
    print("Registration successful")
    print(reg_response.text)
else:
    print("Registration failed")

# Log in as the user
login_data = {
    'user': 'a',
    'password': '12'
}
session.get(url)  # Initial GET might be necessary for CSRF token, etc.
login_response = session.post(url, data=login_data)

if login_response.ok:
    print("Login successful")
    print(login_response.text)
else:
    print("Login failed")

# Access the home page
home_response = session.get(url + 'home')
if home_response.ok:
    print('Access to home page successful')
    print(home_response.text)
else:
    print('Access to home page failed')
