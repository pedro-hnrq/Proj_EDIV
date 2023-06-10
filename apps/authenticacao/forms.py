from django import forms as django_forms
from django.contrib.auth import forms, login, authenticate
from .models import Users
from django.core.exceptions import ValidationError


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = Users


class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = Users

# Formulário do Login
class AuthForm(django_forms.Form):
    email = django_forms.EmailField(
        label = "Email",
        max_length = 254,
        widget= django_forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = django_forms.CharField(
            label = "Senha",
            strip = False,
            widget = django_forms.PasswordInput(attrs={'class': 'form-control'})
    )

    error_messages = {
        'invalid_login': 'Usuário ou senha inválidos',
        'inactive': 'Usuário inátivo',
    }

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        self.user = authenticate(username=email, password=password)

        if not self.user:
            raise self.get_invalid_login_error()
        else:
            self.confirm_user_active()
        return self.cleaned_data

    def log_into(self, request):
        if not self.user:
            raise TypeError('self.user não pode ser None, execute form.is_valid() primeiro')

        login(request, self.user)
        return self.user

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
        )

    # Verificar se usuário está Ativo

    def confirm_user_active(self):
        if not self.user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

# Formulário do Register/Cadastrar
class RegisterForm(UserCreationForm):
    '''Formulário para cadastro de usuários sem permissões 
    administrativas apartir do Email, first_name e senha'''

    class Meta(UserCreationForm.Meta):
        fields = ('first_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if 'password' in field:
                self.fields[field].help_text = None
            self.fields[field].widget.attrs.update({'class': 'form-control'})