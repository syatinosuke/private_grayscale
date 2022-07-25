from turtle import title
from django.core.exceptions import ValidationError

def validate_admin(value):
    if 'admin' in value:
        raise ValidationError('「admin」はメールアドレスに利用できません')
