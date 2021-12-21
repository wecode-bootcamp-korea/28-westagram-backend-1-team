import json
import re

from django.core.exceptions import ValidationError
from django.shortcuts   import render
from django.http    import JsonResponse
from django.views   import View
from users.models   import User


## 이메일 조건 검사
def validate_email(email):
    pattern = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern,email):
        raise ValidationError('EMAIL_VALIDATION')

## 패스워드 조건 검사
def validate_password(password):
    pattern = '^[0-9a-z~!@#$%^&*()_+A-Z]*.{8,}$'
    if not re.match(pattern,password):
        raise ValidationError('PASSWORD_VALIDATION')

class SignupView(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            if not data['email'] or not data['password']:
                return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

            # 이메일 중복 여부 검사
            elif User.objects.filter(email = data['email']):
                return JsonResponse({'message' : 'EMAIL_DUPLICATE_VALUES'}, status = 400)

            validate_email(data['email'])
            validate_password(data['password'])

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        except ValidationError as e:
            return JsonResponse({'message':e.message}, status=400)

        else:
            User.objects.create(
                name          = data['name'],
                email         = data['email'],
                password      = data['password'],
                phone_number  = data['phone_number'],
                date_of_birth = data['date_of_birth']
            )
            return JsonResponse({'message': 'CREATED'}, status=201)
