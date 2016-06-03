#coding: utf8
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, lastname="", firstname=""):
        if not email:
            raise ValueError('Email непременно должен быть указан')
        email=UserManager.normalize_email(email)
        user = self.model( 
            email=email
        )
        

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class ExtUser(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(
        '',
        max_length=255,
        unique=True,
        db_index=True
    )

    avatar = models.CharField(max_length=250)
    
    forgotKey = models.CharField(max_length=150)
    
    firstname = models.CharField(
        '',
        max_length=40,
        null=True,
        blank=True
    )
    lastname = models.CharField(
        '',
        max_length=40,
        null=True,
        blank=True
    )
    date_of_birth = models.DateField(
        'Date birthday',
        auto_now_add=True,
        null=True,
        blank=True
    )
    register_date = models.DateField(
        'Date register',
        auto_now_add=True
    )
    is_active = models.BooleanField(
        'Activate',
        default=True
    )
    is_admin = models.BooleanField(
        'Superuser',
        default=False
    )
    
    
    def createUserForViews(self, email, password, lastname, firstname):
        self.email = UserManager.normalize_email(email)
        self.password = UserManager.set_password(password)
        self.lastname = lastname
        self.firstname = firstname
        return None
        
    
    # Этот метод обязательно должен быть определён
    def get_full_name(self):
        return self.email

    # Требуется для админки
    @property
    def is_staff(self):
        return self.is_admin

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'