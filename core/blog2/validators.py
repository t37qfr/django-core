#custom validation
from django.core.exceptions import ValidationError

def validate_author_email(value):
    if not "@" in value:
        raise ValidationError('Not a valid Email')
    return value
