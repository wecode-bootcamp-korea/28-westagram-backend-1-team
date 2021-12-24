import json
import re
import bcrypt
import jwt

from django.core.exceptions import ValidationError
from django.shortcuts   import render
from django.http    import JsonResponse
from django.views   import View
from users.models   import User
from django.conf    import settings

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

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

            User.objects.create(
                name          = data['name'],
                email         = data['email'],
                password      = hashed_password.decode('utf-8'),
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
        
        try:
            data = json.loads(request.body)

            if not User.objects.filter(email = data['email']).exists():
                raise ValidationError('INVALID_USER')
            
            user = User.objects.filter(email = data['email']).get()

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                raise ValidationError('INVALID_USER')
            
            access_token = jwt.encode({'user_id': user.id}, settings.SECRET_KEY, settings.ALGORITHM)

            return JsonResponse({"MESSAGE":"SUCCESS", "ACCESS_TOKEN": access_token}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE": "JSONDecodeError"}, status=404)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        except ValidationError as e:
            return JsonResponse({'message':e.message}, status=401)