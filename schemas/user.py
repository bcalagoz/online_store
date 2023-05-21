register_login_schema = {
    'type': 'object',
    'properties': {
        "username": {
            "type": "string",
            "description": "Username",
            "maxLength": 255,
            "pattern": "^[a-zA-Z0-9_.-]+$"  # Only letters, numbers, underscores, dots and dashes are allowed
        },
        "password": {
            "type": "string",
            "description": "The user's password.",
            # Minimum eight characters, at least one letter and one number
            "pattern": "^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$",
            "maxLength": 100
        },
    },
    'required': ['username', 'password']
}
