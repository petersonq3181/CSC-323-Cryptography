import requests
import crypto 
import server 

url = 'http://0.0.0.0:8080/'
master_key = b'\xc9\xa3\xb6\xa1mE\xca\xfa\x82\xac\x1e\x17hL\x99\xec'

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
    # print('gg')
    # print(bytes.fromhex(c1), type(bytes.fromhex(c1)))
    print()
    print(type(c1), c1)
    print(type(c2), c2)

    combined_cookie_hex = c1.hex()[:64] + c2.hex()[32:]
    combined_cookie = bytes.fromhex(combined_cookie_hex)
    # print('Combined Cookie Decrypted: ', decrypt_cookie(combined_cookie, master_key))

    # print(crypto.verify_crypto_cookie(bytes.fromhex(c2.hex()), master_key))
    print(crypto.verify_crypto_cookie(combined_cookie, master_key))
    # web.setcookie('auth_token', combined_cookie)

    # # Set the 'auth_token' cookie in the session
    # cookies = {'auth_token': combined_cookie_hex_str}
    # response = requests.get(url, cookies=cookies)

    # session.cookies.set('auth_token', combined_cookie_hex_str)

    # # Now you can make requests as an admin
    # response = session.get(url + 'home')
    # print(response.text)

    # homeresponse = session.get(url)
    # if homeresponse.ok:
    #     print("accessing home page")
    #     print(homeresponse.text)
    # else:
    #     print("failed to access home page")


    # print(response.text)

    # # You can now make requests with the session that uses the new combined cookie
    # # For example, to access a protected page:
    # protected_page_response = session.get(url + 'protected_page')
    # if protected_page_response.ok:
    #     print("Accessed protected page")
    #     print(protected_page_response.text)
    # else:
    #     print("Failed to access protected page")
