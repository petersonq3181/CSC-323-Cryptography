import base64


# Task I. A. Implement Common Encoders & Decoders
def bytes2hex(s):
    return s.hex()

def hex2bytes(s):
    return bytes.fromhex(s)

def base642bytes(s):
    return base64.b64decode(s)

def bytes2base64(s):
    return base64.b64encode(s).decode('utf-8')


byte_string = b"Hello, world!"
hex_string = bytes2hex(byte_string)
print("Hex Encoded:", hex_string)
decoded_bytes = hex2bytes(hex_string)
print("Decoded Bytes:", decoded_bytes)

base64_str = bytes2base64(byte_string)
print("Base64 Encoded:", base64_str)
decoded_bytes = base642bytes(base64_str)
print("Decoded Bytes:", decoded_bytes)

