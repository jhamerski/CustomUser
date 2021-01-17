from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UsuarioManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        # extra_fields.setdefault('is_staff', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super User precisar ser TRUE')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super User precisar ser IS_STAFF')

        return self._create_user(email, password, **extra_fields)


class CustomUsuario(AbstractUser):
    email = models.EmailField('E-mail/login', unique=True)
    telefone = models.CharField('Telefone', max_length=50)
    cpf = models.CharField('Cpf', max_length=20)
    is_staff = models.BooleanField('Membro da equipe', default=True)
    first_name = models.CharField('Primeiro Nome', max_length=50)
    last_name = models.CharField('Último Nome', max_length=50)
    last_login = models.DateTimeField('Último login')
    date_joined = models.DateTimeField('Cadastrado em')

    # Campo que faz acesso ao login, juntamente com senha
    USERNAME_FIELD = 'email'
    # Campos solicitados no cadastro
    REQUIRED_FIELDS = ['first_name', 'last_name', 'cpf', 'telefone']

    def __str__(self):
        return self.email

    objects = UsuarioManager()
