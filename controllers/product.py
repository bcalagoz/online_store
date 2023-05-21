from flask import jsonify, request
from models.product import Product
from models.category import Category
from controllers import login_required
from schemas.product import create_product_schema, update_product_schema
from schemas import validate_json


@login_required(['admin', 'client'])
def get_all_products():
    try:
        products = Product.objects(in_stock=True, amount_in_stock__gte=1)
        result = []
        for product in products:
            product_dict = {
                'id': str(product.id),
                'amount_in_stock': product.amount_in_stock,
                'in_stock': product.in_stock,
                'name': product.name,
                'price': product.price,
                'category': product.category.name
            }
            result.append(product_dict)
        return jsonify({'products': result})

    except Exception as e:
        return jsonify({'error': 'An error occurred: {}'.format(str(e))}), 500


@login_required(['admin'])
@validate_json(create_product_schema)
def create_product():
    try:
        body = request.get_json()
        name = body.get('name')
        amount_in_stock = body.get('amount_in_stock')
        price = body.get('price')
        in_stock = body.get('in_stock')
        category_name = body.get('category')

        category = Category.objects.get(name=category_name)
        body['category'] = category

        Product(name=name,amount_in_stock=amount_in_stock,price=price,in_stock=in_stock,category=category).save()

        return jsonify({'message': 'Product created successfully'}), 200

    except KeyError as e:
        return jsonify({'error': 'Missing key in request data: {}'.format(str(e))}), 400
    except Category.DoesNotExist:
        return jsonify({'error': 'Category not found'}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred: {}'.format(str(e))}), 500


@login_required(['admin'])
@validate_json(update_product_schema)
def update_product(product_id):
    try:
        body = request.get_json()
        product = Product.objects.filter(id=product_id).first()

        if not product:
            return jsonify({'error': 'Product not found.'}), 404

        product.update(**body)

        return jsonify({'message': 'Product successfully updated.', 'id': str(product.id)}), 200

    except KeyError as e:
        return jsonify({'error': 'Missing key in request data: {}'.format(str(e))}), 400
    except Product.DoesNotExist:
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred: {}'.format(str(e))}), 500


@login_required(['admin'])
def delete_product(product_id):
    try:
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return jsonify({'error': 'Product not found.'}), 404
        product.delete()
        return jsonify({'message': 'Product successfully deleted.', 'id': str(product.id)}), 200

    except Product.DoesNotExist:
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred: {}'.format(str(e))}), 500


@login_required(['admin', 'client'])
def filter_products_by_category():
    try:
        category_name = request.args.get('category')
        if not category_name:
            return jsonify({'error': 'Category parameter is missing.'}), 400

        category = Category.objects.get(name=category_name)
        products = Product.objects(category=category)

        result = []
        for product in products:
            product_dict = {
                'id': str(product.id),
                'amount_in_stock': product.amount_in_stock,
                'in_stock': product.in_stock,
                'name': product.name,
                'price': product.price,
                'category': product.category.name
            }
            result.append(product_dict)

        return jsonify({'products': result}), 200

    except Category.DoesNotExist:
        return jsonify({'error': 'Category not found.'}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred: {}'.format(str(e))}), 500

