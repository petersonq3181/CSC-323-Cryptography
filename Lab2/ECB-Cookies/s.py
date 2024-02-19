import requests

url = 'http://0.0.0.0:8080/'

# Create a session object
with requests.Session() as session:
    
    # Register user
    reg_data = {
        'user': 'a', 
        'password': '12' 
    }
    session.get(url + 'register')  # Get the register page to set initial cookies
    reg_response = session.post(url + 'register', data=reg_data)
    
    if reg_response.ok:
        print("Registration successful")
        print(reg_response.text)
    else:
        print("Registration failed")

    # Login as the registered user
    login_data = {
        'user': 'a', 
        'password': '12' 
    }
    session.get(url)  # Get the main page to set initial cookies
    login_response = session.post(url, data=login_data)
    
    if login_response.ok:
        print("Login successful")
        print(login_response.text)
    else:
        print("Login failed")

    # Access home page
    home_response = session.get(url + 'home')
    if home_response.ok:
        print("Accessing home page")
        print(home_response.text)
    else:
        print("Failed to access home page")

    # Get cookie
    cookie_response = session.get(url + 'get_cookie')
    print("Cookie:", cookie_response.text)
