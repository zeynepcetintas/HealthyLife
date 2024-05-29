from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    mobile = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'second_name', 'age', 'height', 'weight', 'mobile', 'gender']

    objects = UserManager()

    def __str__(self):
        return self.email
