from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("Dude you need a username.")
        if not email:
            raise ValueError("type an e-mail..")

        new_user = self.model(
            username=username, email=CustomUserManager.normalize_email(email)
        )
        new_user.set_password(password)
        new_user.is_staff = True
        new_user.save(using=self._db)
        return new_user

    def create_superuser(self, username, email, password):
        new = self.create_user(username, email, password=password)
        new.is_active = True
        new.is_staff = True
        new.is_superuser = True
        new.save(using=self._db)
        return new
