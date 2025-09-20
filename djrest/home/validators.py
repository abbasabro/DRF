from rest_framework.validators import ValidationError

def no_name(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('Name Doesnot Contain Number')