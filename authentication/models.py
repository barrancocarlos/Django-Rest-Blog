from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.

class ProfileManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        # Ensure that an email address is set
        if not email:
            raise ValueError('Users must have a valid e-mail address')

        account = self.model(
            email=self.normalize_email(email),
            username= kwargs['username'],
        )
        account.set_password(password)
        account.save(using=self._db)
        return account

    def create_superuser(self, email, username, password=None):
        account = self.create_user(email=email, password=password, username=username)
        account.is_admin = True        
        account.save(using=self._db)
        return account
        
class Profile(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    username = models.CharField(max_length=50, unique=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    password_expire = models.BooleanField(default=False)
    password_expire_date = models.DateTimeField(auto_now_add=True)
    #token_generated = models.CharField(max_length=50, null=True, blank=True, default=None)

    objects = ProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
