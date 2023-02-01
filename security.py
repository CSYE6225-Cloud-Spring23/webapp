import base64
import bcrypt

import re

def get_encoded_token(password):
    print (password)

    token = bytes.decode(base64.b64encode(bytes(password.encode())))

    return token


def get_bcrypt_password(password):

    salt = bcrypt.gensalt()
    hashed = bytes.decode(bcrypt.hashpw(bytes(password.encode()), salt))
    return hashed

def email_validation(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if re.match(regex, email):
        return True
    return False