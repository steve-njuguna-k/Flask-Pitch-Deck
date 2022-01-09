from itsdangerous import URLSafeTimedSerializer
from flask import app
from .config import SECRET_KEY, SQLALCHEMY_DATABASE_URI

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt = SQLALCHEMY_DATABASE_URI)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt = SQLALCHEMY_DATABASE_URI,
            max_age = expiration
        )
    except:
        return False
    return email