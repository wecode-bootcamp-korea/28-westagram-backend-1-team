import re
import json
import bcrypt

from django.http            import JsonResponse
from django.views           import View
from users.models           import User
from users.validation       import validate_email, validate_password
from django.core.exceptions import ValidationError

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            validate_email(data['email'])
            validate_password(data['password'])
            
            User.objects.create(
                name         = data['name'],
                email        = data['email'],
                password     = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                phone_number = data['phone_number'],
            )
                    
            return JsonResponse({'message': "SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({'message': "KEY_ERROR"}, status=400)
        except ValidationError as e:
            return JsonResponse({'message': str(e.message)}, status=400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            if data['email'] == '' or data['password'] == '':
                return JsonResponse({"message": "EMPTY_VALUE"}, status=401)
                
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "INVALID_EMAIL"}, status=401)
                
            user = User.objects.get(email=data['email'])
        
            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=401)
                
            return JsonResponse({"message": "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
