from django.db import models

class User(models.Model):
    name               = models.CharField(max_length=20)
    email              = models.EmailField(max_length=128, unique= True)
    password           = models.CharField(max_length=300)
    phone_number       = models.CharField(max_length = 20, unique = True)
    date_of_birth      = models.DateField(null = True)
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
