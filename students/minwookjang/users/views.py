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

def login_email_check(email):

    if not User.objects.filter(email = email):
        raise ValidationError('INVALID_USER')

def login_password_check(email,password):

    if not User.objects.filter(email = email, password = password):
        raise ValidationError('INVALID_USER')

class SignupView(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(email = data['email']):
                return JsonResponse({'message' : 'EMAIL_DUPLICATE_VALUES'}, status = 400)

            validate_email(data['email'])
            validate_password(data['email'],data['password'])

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

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            login_email_check(data['email'])
            login_password_check(data['email'],data['password'])
            
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        except ValidationError as e:
            return JsonResponse({'message':e.message}, status=401)
    
        return JsonResponse({'message': 'SUCCESS'}, status=200)