import mongoengine as db
from models.user import User


class Auth(db.Document):
    user = db.ReferenceField(User, required=True)
    token_type = db.StringField(default="access", required=True)
    session_key = db.StringField(required=True)
    created_at = db.DateTimeField(auto_now_add=True)
