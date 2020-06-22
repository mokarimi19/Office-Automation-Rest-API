from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password=None):
        if not username:
            raise ValueError("you need a username.")
        if not email:
            raise ValueError("type an e-mail..")
        if not first_name:
            raise ValueError("your first_name!?!")
        if not last_name:
            raise ValueError("fill out  last_name!?!")
        new_user = self.model(
            username=username, email=CustomUserManager.normalize_email(email),
            first_name=first_name, last_name=last_name
        )
        new_user.set_password(password)
        new_user.is_staff = True
        new_user.save(using=self._db)
        return new_user

    def create_superuser(self, username, email, first_name, last_name, password):
        new = self.create_user(
            username, email, first_name, last_name, password=password
        )
        new.is_active = True
        new.is_staff = True
        new.is_superuser = True
        new.save(using=self._db)
        return new
