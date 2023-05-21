from flask import Flask, jsonify
from routes.user import auth_bp
from routes.product import product_bp
from routes.category import category_bp
from routes.cart import cart_bp
from flask_mongoengine import MongoEngine
import os


app = Flask(__name__)


app.config['MONGODB_SETTINGS'] = {
    "db": os.getenv("DATABASE_NAME"),
    "host": os.getenv("DATABASE_HOST"),
    "port": int(os.getenv("DATABASE_PORT"))
}

db = MongoEngine(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(product_bp, url_prefix='/product')
app.register_blueprint(category_bp, url_prefix='/category')
app.register_blueprint(cart_bp, url_prefix='/cart')


@app.route('/')
def hello_world():  # put application's code here
    return jsonify({'message': 'Hello World!'})


if __name__ == '__main__':
    app.run()
