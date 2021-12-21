import json, re

from django.views import View
from django.http  import JsonResponse

from users.models import User

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']

            email_regex    = '[a-zA-Z0-9.-_+]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+'
            password_regex = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

            if not re.match(email_regex, data['email']):
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)

            if not re.match(password_regex, data['password']):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)
       
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message' : 'ALREADY_EXIST'}, status = 400)

            User.objects.create(
                email         = data['email'],
                password      = data['password'],
                name          = data['name'],
                mobile_number = data['mobile_number']
                )
            return JsonResponse({'message' : 'SUCCESS'}, status = 201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

class LogInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body) 

            email    = data['email']
            password = data['password']
          
            if not User.objects.filter(email=data['email']).exists() \
               or not User.objects.filter(password=data['password']).exists():
                return JsonResponse({'message' : 'INVALID_USER'}, status = 401)

            if User.objects.get(email=data['email']).password != password:
                return JsonResponse({'message' : 'INVALID_USER'}, status = 401)

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)            
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)