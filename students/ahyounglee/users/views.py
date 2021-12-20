import json
import re

# from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from .models import User
# Create your views here.
'''
username : "이아영"
email : "dkdud2408@gmail.com"
password : "1234"
phone_number : 01035460692
is_professional : False

---------------
'''
class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            email    = data['email']
            password = data['password']

            if re.match("/^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i;", email) == None:
                return JsonResponse({"message": "Validation_ERROR"}, status=400)
            elif re.match("/^.*(?=^.{8,15}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&+=]).*$/;", password) == None:
                return JsonResponse({"message": "Validation_ERROR"}, status=400)
            else:
                signup = User.objects.create(
                    username        = data['username'],
                    email           = data['email'],
                    password        = data['password'],
                    phone_number    = data['phone_number'],
                    is_professional = data['is_professional']
                )

            return JsonResponse({'message' : 'created'}, status=201)

        except :
            return JsonResponse({"message": "KEY_ERROR"}, status=400)