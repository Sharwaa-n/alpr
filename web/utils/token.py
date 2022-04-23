import jwt
import datetime
from .config import env

dir(jwt)

def encode(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            env('APP_SECRET'),
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode(auth_token):
    try:
        payload = jwt.decode(auth_token, env('APP_SECRET'))
        print('Token:', auth_token, payload)
        return (True, payload['sub'])
    except jwt.ExpiredSignatureError:
        return (False, 'Signature expired. Please log in again.')
    except jwt.InvalidTokenError:
        return (False, 'Invalid token. Please log in again.')