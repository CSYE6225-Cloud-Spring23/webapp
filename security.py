import base64
import bcrypt

def get_encoded_token(password):
    print (password)

    token = bytes.decode(base64.b64encode(bytes(password.encode())))

    return token


def get_bcrypt_password(password):

    salt = bcrypt.gensalt()
    hashed = bytes.decode(bcrypt.hashpw(bytes(password.encode()), salt))
    return hashed