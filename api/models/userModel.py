from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = [
    (1, "EMPLOYEE"),
    (2, "EMPLOYER"),
]

class UserModel(AbstractUser):
    role = models.IntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_picture = models.ImageField(upload_to="company_pictures", blank=True, null=True)

    class Meta:
        db_table = "User"