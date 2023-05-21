import mongoengine as db
from models.category import Category


class Product(db.Document):
    name = db.StringField(required=True)
    amount_in_stock = db.IntField(required=True)
    price = db.FloatField(required=True)
    in_stock = db.BooleanField(default=True)
    category = db.ReferenceField(Category, required=True)





