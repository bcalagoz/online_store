cart_schema = {
    'type': 'object',
    'properties': {
        "user_id": {
            "type": "string",
            "description": "Id of the user"
        },
        "product_id": {
            "type": "string",
            "description": "Id of the product",
        },
    },
    'required': ['user_id', 'product_id']
}