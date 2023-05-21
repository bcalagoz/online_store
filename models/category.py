import mongoengine as db


class Category(db.Document):
    name = db.StringField(required=True, unique=True)
