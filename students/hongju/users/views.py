import json
import re

from django.http      import JsonResponse
from django.views     import View
from users.models     import User
from users.validation import *

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        is_valid_email = validate_email(data['email'])
        is_valid_pw = validate_pw(data['password'])
        
        try:
            if is_valid_email == 'empty' or is_valid_pw == 'empty':
                return JsonResponse({'message': "KEY_ERROR"}, status=400)
                
            if is_valid_email == 'duplicate_email':
                return JsonResponse({'message': "ERROR_EMAIL_ALREADY_EXIST"}, status=400)
                
            if is_valid_email == 'no_match':
                return JsonResponse({'message': "ERROR_EMAIL_NEED_@AND."}, status=400)
                
            if is_valid_pw == 'no_match':
                return JsonResponse({'message': "ERROR_REQUIRE_8_LETTER,NUMBER,SPECIAL_SYMBOLS)"}, status=400)
        
            if is_valid_email and is_valid_pw:
                User.objects.create(
                        name         = data['name'],
                        email        = data['email'],
                        password     = data['password'],
                        phone_number = data['phone_number'],
                        )
                    
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        except KEY_ERROR:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        


