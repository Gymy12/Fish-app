from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# Create your models here.
class Gender(models.Model):
    gender = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.gender


class UserManager(BaseUserManager):
    def create_user(
        self,
        first_name,
        last_name,
        gender,
        email,
        location_address,
        phone=None,
        password=None,
    ):
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not phone:
            raise ValueError("Users must have a phone number")
        if not email:
            raise ValueError("Users must have an email")
        # if not id_passport_number:
        #     raise ValueError("Users must have an ID/Passport number")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone=phone,
            email=self.normalize_email(email),
            location_address=location_address,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        first_name,
        last_name,
        gender,
        email,
        location_address,
        phone=None,
        password=None,
    ):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone=phone,
            email=self.normalize_email(email),
            location_address=location_address,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserTypes(models.Model):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"
    EMPLOYEE = "EMPLOYEE"

    USER_TYPES_CHOICES = (
        (ADMIN, "Admin"),
        (CUSTOMER, "Customer"),
        (EMPLOYEE, "Employee"),
    )

    user_type = models.CharField(
        max_length=9, choices=USER_TYPES_CHOICES, default=CUSTOMER
    )

    def __str__(self):
        return self.user_type


class CustomerUser(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.ForeignKey(
        Gender, on_delete=models.SET_NULL, null=True, blank=False, default=None
    )
    phone = models.CharField(max_length=15, unique=True, blank=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    user_type = models.ForeignKey(UserTypes, on_delete=models.SET_NULL, null=True)
    dp = models.ImageField(upload_to="dp", blank=True, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email + " : " + self.first_name + " " + self.last_name

    def groups(self):
        pass

    def user_permissions(self):
        pass

    class Meta:
        swappable = "AUTH_USER_MODEL"
