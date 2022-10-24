from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email=self.normalize_email(email)

        user=self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Supeuser has to have is_staff true")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Supeuser has to have is_superuser true")    

        return self.create_user(email=email, password=password, **extra_fields) 

class User(AbstractUser):
    email = models.CharField(max_length=200, unique=True)
    username = models.CharField(max_length=200)    
    address = models.CharField(max_length=200)    
    phone_number = PhoneNumberField()

    is_production_staff=models.BooleanField(default=False)
    is_store_staff=models.BooleanField(default=False)
    is_sales_staff=models.BooleanField(default=False)
    is_branch_staff=models.BooleanField(default=False)
    is_site_staff=models.BooleanField(default=False)
    is_dispatch_staff=models.BooleanField(default=False)
    is_dispatch_staff=models.BooleanField(default=False)
    is_procurement_staff=models.BooleanField(default=False)




    # is_social_media_staff=models.BooleanField(default=False)


    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username','phone_number']

    def __str__(self):
        return self.email

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
#     bio = models.TextField(null=True)
#     position = models.CharField(max_length=300, null=True)
#     image = models.FileField(upload_to='users/images', null=True)
#     duties = models.TextField(null=True)

#     def __str__(self):
#         return self.position
