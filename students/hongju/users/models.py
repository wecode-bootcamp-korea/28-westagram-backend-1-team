from django.db import models

# Create your models here.
class User(models.Model):
    name         = models.CharField(max_length=45)
    email        = models.CharField(max_length=300)
    password     = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=45)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user"
