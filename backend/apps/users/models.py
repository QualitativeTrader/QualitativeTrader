from django.db import models

class Account(models.Model):
    email = models.EmailField(max_length=50)
    auth_password = models.CharField(max_length=32)
    is_auth = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)