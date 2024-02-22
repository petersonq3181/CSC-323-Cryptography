import requests
import crypto 
from server import master_key

url = 'http://0.0.0.0:8080/'

with requests.Session() as session:

    def reg_and_login(username, password):
        c1data = {
            'user': username, 
            'password': password 
        }
        session.get(url + 'register') 
        c1response = session.post(url + 'register', data=c1data)
        
        # if c1response.ok:
        #     print("registration successful")
        #     print(c1response.text)
        # else:
        #     print("registration failed")

        session.get(url)
        c1loginresponse = session.post(url, data=c1data)
        
        # cookie = ''
        if c1loginresponse.ok:
            # print("login successful")
            # print(c1loginresponse.text)
            cookie = session.cookies.get_dict().get('auth_token')
            print('gg', type(cookie), cookie)
        #     print("cookies after login:", cookie)
        # else:
        #     print("login failed")

        # homeresponse = session.post(url)
        # if homeresponse.ok:
        #     print("accessing home page")
        #     print(homeresponse.text)
        # else:
        #     print("failed to access home page")

        return cookie
    
    c1 = bytes.fromhex(reg_and_login('123456789012345', '1'))
    c2 = bytes.fromhex(reg_and_login('12345678901admin', '2'))

    combined_cookie_hex = c1.hex()[:64] + c2.hex()[32:]
    combined_cookie = bytes.fromhex(combined_cookie_hex)

    # print(type(master_key), master_key)

    # print(crypto.verify_crypto_cookie(combined_cookie, master_key))
    
    # session.cookies.set('auth_token', combined_cookie_hex)
    res = session.post(url + 'verify', data={'cookie_value': combined_cookie_hex})

    cookie = session.cookies.get_dict().get('auth_token')
    print('gg', type(cookie), cookie)

    res = session.get(url + 'verify')
    print(res.text)