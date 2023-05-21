import mongoengine as db
from models.product import Product
from models.user import User


class Cart(db.Document):
    user = db.ReferenceField(User, required=True)
    selected_products = db.ListField(db.ReferenceField(Product))
    count = db.IntField(required=True)
    total_price = db.FloatField(required=True)
