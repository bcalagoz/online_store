from flask import jsonify, request
from models.category import Category
from mongoengine.errors import NotUniqueError
from controllers import login_required
from schemas.category import category_schema
from schemas import validate_json


@login_required(['admin'])
def get_all_category():
    try:
        categories = Category.objects()
        result = []
        for category in categories:
            category_json = {
                'id': str(category.id),
                'name': category.name
            }
            result.append(category_json)
        return jsonify({'categories': result})
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'message': str(e)}), 500


@login_required(['admin'])
@validate_json(category_schema)
def create_category():
    try:
        body = request.get_json()
        category_name = body['name']
        Category(name=category_name).save()
        return jsonify({'message': 'Category successfully created.'}), 200

    except KeyError as e:
        return jsonify({'error': 'Missing key in request data: {}'.format(str(e))}), 400

    except NotUniqueError as e:
        return jsonify({'error': 'Category name is not unique'}), 400

    except Exception as e:
        return jsonify({'error': 'An error occurred: {}'.format(str(e))}), 500


@login_required(['admin'])
@validate_json(category_schema)
def update_category(category_id):
    try:
        body = request.get_json()
        category = Category.objects.filter(id=category_id).first()
        if not category:
            return jsonify({'error': 'Category not found.'}), 404
        category.update(**body)
        return jsonify({'message': 'Category successfully updated.', 'id': str(category.id)}), 200

    except KeyError as e:
        return jsonify({'error': 'Missing key in request data: {}'.format(str(e))}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred: {}'.format(str(e))}), 500


@login_required(['admin'])
def delete_category(category_id):
    try:
        category = Category.objects.filter(id=category_id).first()
        if not category:
            return jsonify({'error': 'Category not found.'}), 404
        category.delete()
        return jsonify({'message': 'Category successfully deleted.', 'id': str(category.id)}), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred', 'message': str(e)}), 500
