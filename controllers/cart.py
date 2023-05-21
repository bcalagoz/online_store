from flask import jsonify, request
from models.user import User
from models.cart import Cart
from models.product import Product
from controllers import login_required
from schemas.cart import cart_schema
from schemas import validate_json


@login_required(['admin', 'client'])
@validate_json(cart_schema)
def add_to_cart():
    try:
        data = request.get_json()
        user_id = data['user_id']
        product_id = data['product_id']

        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)

        cart = Cart.objects(user=user).first()
        if cart:
            if product not in cart.selected_products:
                cart.selected_products.append(product)
                cart.count += 1
                cart.total_price += product.price
                cart.save()
        else:
            cart = Cart(user=user, selected_products=[product], count=1, total_price=product.price)
            cart.save()

        return jsonify({'message': 'Product added to cart successfully'}), 200

    except KeyError as e:
        return jsonify({'error': 'Missing key in request data: {}'.format(str(e))}), 400
    except User.DoesNotExist:
        return jsonify({'error': 'User not found'}), 404
    except Product.DoesNotExist:
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred: {}'.format(str(e))}), 500


@login_required(['admin', 'client'])
@validate_json(cart_schema)
def remove_from_cart():
    try:
        data = request.get_json()
        user_id = data['user_id']
        product_id = data['product_id']

        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)

        cart = Cart.objects(user=user).first()
        if cart:
            if product in cart.selected_products:
                cart.selected_products.remove(product)
                cart.count -= 1
                cart.total_price -= product.price
                cart.save()

                if cart.count == 0:
                    cart.delete()

        return jsonify({'message': 'Product removed from cart successfully'}), 200

    except KeyError as e:
        return jsonify({'error': 'Missing key in request data: {}'.format(str(e))}), 400

    except User.DoesNotExist:
        return jsonify({'error': 'User not found'}), 404
    except Cart.DoesNotExist:
        return jsonify({'error': 'There is no cart'}), 404
    except Product.DoesNotExist:
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred: {}'.format(str(e))}), 500


@login_required(['admin', 'client'])
def get_products_in_cart(user_id):
    try:
        user = User.objects.get(id=user_id)
        cart = Cart.objects(user=user).first()

        if cart:
            products = []
            for product in cart.selected_products:
                products.append({
                    'id': str(product.id),
                    'name': product.name,
                    'amount_in_stock': product.amount_in_stock,
                    'price': product.price,
                    'in_stock': product.in_stock,
                    'category': product.category.name
                })

            return jsonify({'products': products}), 200
        else:
            return jsonify({'message': 'No products in the cart'}), 404
    except KeyError as e:
        return jsonify({'error': 'Missing key in request data: {}'.format(str(e))}), 400
    except User.DoesNotExist:
        return jsonify({'error': 'User not found'}), 404
    except Cart.DoesNotExist:
        return jsonify({'error': 'There is no cart'}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred: {}'.format(str(e))}), 500