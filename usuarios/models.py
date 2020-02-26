from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager


class UsuarioManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('O Username/E-mail é obrigatório')
        user = self.model(email=username, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        # Comentado pois o ideal é habilitar após a confirmação do e-mail caso usuario seja membro da equipe
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')

        return self._create_user(username, password, **extra_fields)


class CustomUsuario(AbstractUser):
    # Sobrescrito models de username para criar campo que já valide o e-mail digitado
    username = models.EmailField('Username/E-mail', unique=True)
    # Criado atributo fone e do mesmo modo posso criar quantos atributos forem necessarios
    fone = models.CharField('Telefone', max_length=15)
    is_staff = models.BooleanField('Membro da equipe', default=True)

    # Foi necessario sobrescrever esses 2 atributos para fazer eles ficarem obrigatorios
    first_name = models.CharField('Primeiro nome', max_length=30, blank=False)
    last_name = models.CharField('Último nome', max_length=150, blank=False)

    # Preciso especificar meu gerenciador personalizado, senão django usará o seu padrão
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    # Verificar por que não tornou estes 3 campos obrigatorios
    REQUIRED_FIELDS = ['first_name', 'last_name', 'fone']

    def __str__(self):
        return self.username
