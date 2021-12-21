import json
import re

from django.core.exceptions import ValidationError
from django.shortcuts   import render
from django.http    import JsonResponse
from django.views   import View
from users.models   import User

def validate_email(email):
    REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if not re.match(REGEX_EMAIL,email):
        raise ValidationError('EMAIL_VALIDATION')

def validate_password(password):
    REGEX_PASSWORD = '^[0-9a-z~!@#$%^&*()_+A-Z]*.{8,}$'
    
    if not re.match(REGEX_PASSWORD,password):
        raise ValidationError('PASSWORD_VALIDATION')

class SignupView(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(email = data['email']):
                return JsonResponse({'message' : 'EMAIL_DUPLICATE_VALUES'}, status = 400)

            validate_email(data['email'])
            validate_password(data['password'])

            User.objects.create(
                name          = data['name'],
                email         = data['email'],
                password      = data['password'],
                phone_number  = data['phone_number'],
                date_of_birth = data['date_of_birth']
            )
            return JsonResponse({'message': 'CREATED'}, status=201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        except ValidationError as e:
            return JsonResponse({'message':e.message}, status=400)
