from itsdangerous import URLSafeTimedSerializer

import config
# from db import User
import db

serializer = URLSafeTimedSerializer(config.SECRET_KEY)


def generate_activation_token(user):
    data = [user.get_id(), user.username, user.email]
    return serializer.dumps(data)


def get_user_by_activation_token(token, max_age=config.ACTIVATION_TOKEN_LIFETIME):
    uid, username, email = serializer.loads(token, max_age=max_age)
    user = db.User.objects.get(id=uid)
    if user.username == username and user.email == email:
        return user
    return None
