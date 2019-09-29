from django.db import models
# adding some package to extend django user model while using some of the
#   features that comes with django user model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
# creating manager class
# provides a helper functions to create user or super users


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        """
        Creates and saves a new user
        """
        if not email:
            raise ValueError("User email is requried!")
        user = self.model(email=self.normalize_email(email), **kwargs)
        # the password needs to be encrypted
        user.set_password(password)
        # for supporting multiple databases
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Creates and save a new super user
        :param email:
        :param password:
        :return:
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email instead of username
    """
    #  create one user with one email
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    #  define if user in system in active or not
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    #  assign user manager to objects attribute
    objects = UserManager()  # don't forget bracket to assign new user manger
    #  finally we define user name to email
    USERNAME_FIELD = 'email'
