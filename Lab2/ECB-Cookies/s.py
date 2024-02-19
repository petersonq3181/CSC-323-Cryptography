import requests

url = 'http://0.0.0.0:8080/'

with requests.Session() as session:

    def reg_and_login(username, password):
        c1data = {
            'user': username, 
            'password': password 
        }
        session.get(url + 'register') 
        c1response = session.post(url + 'register', data=c1data)
        
        if c1response.ok:
            print("registration successful")
            print(c1response.text)
        else:
            print("registration failed")

        session.get(url)
        c1loginresponse = session.post(url, data=c1data)
        
        cookie = ''
        if c1loginresponse.ok:
            print("login successful")
            print(c1loginresponse.text)
            cookie = session.cookies.get_dict().get('auth_token')
            print("cookies after login:", cookie)
        else:
            print("login failed")

        homeresponse = session.get(url + 'home')
        if homeresponse.ok:
            print("accessing home page")
            print(homeresponse.text)
        else:
            print("failed to access home page")

        return cookie
    
    c1 = reg_and_login('123456789012345', '1')
    c2 = reg_and_login('12345678901admin', '1')
    print(c1)
    print(c2)

    combined_cookie_hex = c1[:64] + c2[32:]
    combined_cookie = bytes.fromhex(combined_cookie_hex)

