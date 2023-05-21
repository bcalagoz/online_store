import mongoengine as db
from enum import Enum


class RoleEnum(Enum):
    ADMIN = 'admin'
    CLIENT = 'client'


class User(db.Document):
    username = db.StringField(unique=True, required=True)
    password = db.StringField(required=True)
    is_active = db.BooleanField(default=True)
    role = db.EnumField(RoleEnum, default=RoleEnum.CLIENT)
