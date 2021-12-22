from django.urls    import path
from users.views    import SignupView
from users.views    import LoginView


urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/login', LoginView.as_view())
]