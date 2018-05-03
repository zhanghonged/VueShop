from django.apps import AppConfig
from django.db.models.signals import post_save
from .signals import create_user

class UsersConfig(AppConfig):
    name = 'apps.users'
    verbose_name = "用户管理"

    def ready(self):
        import users.signals
        post_save.connect(
            receiver=create_user,
            sender=self.get_model('User')
        )