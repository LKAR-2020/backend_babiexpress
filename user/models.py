from django.contrib.auth.models import AbstractUser , Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    email_verified = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    account_created_at = models.DateTimeField(auto_now_add=True)
    is_courier = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    id_number = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
