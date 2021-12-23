import re
import json

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
                password     = data['password'],
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
                
            if not (User.objects.filter(email=data['email'], password=data['password'])).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)
      
            return JsonResponse({"message": "SUCCESS"}, status=200)
        except KEY_ERROR:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
