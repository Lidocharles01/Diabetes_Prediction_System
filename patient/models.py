from django.db import models

class WebsiteUser(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.EmailField(max_length=67)
    password=models.CharField(max_length=67)
    username=models.CharField(max_length=89)