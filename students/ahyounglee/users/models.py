from django.db import models

class User(models.Model):
    username         = models.CharField(max_length=45)
    email            = models.EmailField(max_length=100)
    passWord         = models.CharField(max_length=256)
    phone_number     = models.CharField(max_length = 40, unique = True)
    is_professional  = models.BooleanField(default=False)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'