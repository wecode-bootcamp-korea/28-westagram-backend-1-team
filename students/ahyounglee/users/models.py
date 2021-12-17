from django.db import models
from django.core.validators import RegexValidator


class User(models.Model):
    username         = models.CharField(max_length=45, blank=False, null=False)
    email            = models.EmailField(max_length=100, blank=False, null=False)
    password         = models.CharField(max_length=256, blank=False, null=False)
    phoneNumberRegex = RegexValidator(regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phone            = models.CharField(validators = [phoneNumberRegex], max_length = 11, unique = True)
    is_professional  = models.BooleanField(default=False)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'



