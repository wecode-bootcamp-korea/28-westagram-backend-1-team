import re

from django.core.exceptions import ValidationError
from users.models           import User

REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

def validate_email(value) :
    if value == '':
        raise ValidationError('EMPTY_EMAIL')
    
    if User.objects.filter(email=value).exists():
        raise ValidationError('USER_ALREADY_EXISTS')
        
    if not re.match(REGEX_EMAIL, value):
        raise ValidationError('INVALID_EMAIL_ADDRESS')

def validate_password(value) :
    if value == '':
        raise ValidationError('EMPTY_PASSWORD')
        
    if not re.match(REGEX_PASSWORD, value):
        raise ValidationError('INVALID_PASSWORD')
