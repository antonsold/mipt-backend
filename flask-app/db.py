from os import getenv
from mongoengine import *
from passlib.apps import custom_app_context as pwd_context
from flask_login import UserMixin

import config
import activation

connect(getenv('MONGO_DB'), host=getenv('MONGO_HOST', 'localhost'))


class User(Document, UserMixin):
    username = StringField(required=True, unique=True)
    email = StringField(required=True)
    password_hash = StringField()
    is_active = BooleanField(required=True, default=False)

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password_hash = pwd_context.hash(password)
    
    def check_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def get_activation_token(self):
        return activation.generate_activation_token(self)
