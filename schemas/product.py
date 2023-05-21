create_product_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'amount_in_stock': {'type': 'integer'},
        'price': {'type': 'number'},
        'in_stock': {'type': 'boolean'},
        'category': {'type': 'string'},
    },
    'required': ['name', 'amount_in_stock', 'price', 'in_stock', 'category']
}

update_product_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'amount_in_stock': {'type': 'integer'},
        'price': {'type': 'number'},
        'in_stock': {'type': 'boolean'},
        'category': {'type': 'string'},
    },
    'required': []
}