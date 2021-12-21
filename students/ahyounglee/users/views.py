import json

# from django.shortcuts import render
from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError

from .models      import User
from .validations import is_email_valid, is_password_valid

class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            username        = data['username']
            email           = data['email']
            password        = data['password']
            phone_number    = data['phone_number']
            is_professional = data['is_professional']

            if is_email_valid(email) == None:
                raise ValidationError('INVALID_EMAIL')
            elif is_password_valid(password) == None:
                raise ValidationError('INVALID_PASSWORD')
            elif User.objects.filter(email=email).exists():
                raise ValidationError('DUPLICATED_EMAIL')
            else:
                User.objects.create(
                    username        = username,
                    email           = email,
                    password        = password,
                    phone_number    = phone_number,
                    is_professional = is_professional
                )

            return JsonResponse({'message' : 'created'}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValidationError as e:
            return JsonResponse({"message": e.message}, status=400)