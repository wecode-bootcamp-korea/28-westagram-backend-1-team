import json
import re

from django.http     import JsonResponse
from django.views    import View
from users.models    import User

# 빈 데이터입력 확인
def check_empty(email_or_pw):
    if email_or_pw == '':
        return True
    else:
        return False
# 이메일 validation
def validate_email(email_data):
    if check_empty(email_data) == True:
        return 'empty'
    
    # 중복 확인
    if User.objects.filter(email=email_data).exists():
        return 'duplicate_email'
    # 매치 확인
    if re.match(r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$", email_data) == None:
        return 'no_match'

    return True

# 비밀번호 validation
def validate_pw(pw_data):
    if check_empty(pw_data) == True:
        return 'empty'
        
    # 매치 확인
    if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*#?&]).{8,}$", pw_data) == None:
        return 'no_match'

    return True

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        isValidEmail = validate_email(data['email'])
        isValidPW = validate_pw(data['password'])
        
        try:
            if isValidEmail == 'empty' or isValidPW == 'empty':
                return JsonResponse({"message": "KEY_ERROR"}, status=400)
                
            if isValidEmail == 'duplicate_email':
                return JsonResponse({"message": "ERROR_EMAIL_ALREADY_EXIST"}, status=400)
                
            if isValidEmail == 'no_match':
                return JsonResponse({"message": "ERROR_EMAIL_NEED_@AND."}, status=400)
                
            if isValidPW == 'no_match':
                return JsonResponse({"message": "ERROR_REQUIRE_8_LETTER,NUMBER,SPECIAL_SYMBOLS)"}, status=400)
        
            if isValidEmail and isValidPW:
                User.objects.create(
                        name         = data['name'],
                        email        = data['email'],
                        password     = data['password'],
                        phone_number = data['phone_number'],
                        )
                    
            return JsonResponse({'Message': 'SUCCESS'}, status=201)
        except:
            return JsonResponse({'message': 'UNKNOWNED_ERROR'}, status=400)
        


