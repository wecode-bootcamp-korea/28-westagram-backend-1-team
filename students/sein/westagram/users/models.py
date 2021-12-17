from django.db import models

class User(models.Model):
    user_name     = models.CharField(max_length=30)
    email         = models.EmailField(max_length=100, unique=True)
    password      = models.CharField(max_length=300)
    mobile_number = models.CharField(max_length=20, unique=True)
    other_info    = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "users"
