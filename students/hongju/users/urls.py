from django.urls import path
from users.views import SignUpView

urlpatterns = [
        path('signUp', SignUpView.as_view())
]

