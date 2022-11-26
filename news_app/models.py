from django.db import models

# Create your models here.
class UserData(models.Model):
    first_name = models.CharField(max_length=30, blank = False)
    last_name = models.CharField(max_length=30, blank = False)
    email = models.CharField(max_length=50, unique = True, blank = False)
    password = models.CharField(max_length=20, blank = False)