from django.db import models
from django.contrib.auth.models import AbstractUser

#Create a custom user model to extend the user functionality

# Create your models here.

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_engineer = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    class Meta:
        # Add or change the related_name for groups and user_permissions
        # to avoid clashes with dashboard.User model
        swappable = 'AUTH_USER_MODEL'
        permissions = [
            ("can_change_user_status", "Can change user status"),
        ]

    def __str__(self):
        return self.username