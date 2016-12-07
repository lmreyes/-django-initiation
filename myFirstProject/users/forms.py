from base.validators import is_password_secure
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, RegexValidator
from django.utils.translation import ugettext_lazy as _
from django_countries.widgets import CountrySelectWidget
from registration.forms import RegistrationForm

from .models import User


class UserRegisterForm(RegistrationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class LoginForm(forms.Form):
    email = forms.CharField(label='', required=True,
                            widget=forms.TextInput(attrs={'placeholder': _('YOUR MAIL')}))
    password = forms.CharField(label='', max_length=32,
                               widget=forms.PasswordInput(attrs={'placeholder': _('YOUR PASSWORD')}),
                               required=True,)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email(email)
        return email

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            try:
                username = get_user_model().objects.get(email=email).username
            except:
                raise forms.ValidationError(_("Sorry, that login was invalid. Please try again."))

            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(_("Sorry, that login was invalid. Please try again."))
            if not user.is_active:
                raise forms.ValidationError(_("Sorry, that login was invalid. Please try again."))
        return self.cleaned_data
