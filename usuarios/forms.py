from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUsuario


# Formulario para criação do usuario
class CustomUsuarioCreateForm(UserCreationForm):

    class Meta:
        model = CustomUsuario
        # Campos que quero apresentar
        fields = ('first_name', 'last_name', 'fone')

        # Forma que quero apresentar para o label de username
        # labels = {'username': 'Username/E-mail'}  # comentado pois username foi sobrescrito no model CustomUsuario()

    def save(self, commit=True):
        user = super().save(commit=False)
        # Pegando senha do campo 1 pois caso nos dois campos sejam iguais a senha será criptografada
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['username'].lower()
        if commit:
            user.save()
        return user


# Formulario para alteração do usuario
class CustomUsuarioChangeForm(UserChangeForm):

    class Meta:
        model = CustomUsuario
        # Campos que quero apresentar
        fields = ('first_name', 'last_name', 'fone')
