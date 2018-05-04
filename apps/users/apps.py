from django.apps import AppConfig
from django.db.models.signals import post_save
from .signals import create_user

class UsersConfig(AppConfig):
    name = 'apps.users'
    verbose_name = "用户管理"