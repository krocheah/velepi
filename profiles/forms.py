from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms

class RegistrationForm(UserCreationForm):
	class Meta:
		fields = ['username', 'email'] #<-- Registiration Formuna default gelen form fieldlarından farklı olarak 'username' ve 'email' fieldlarını da ekledik

		widgets = {
			'email' : forms.TextInput(attrs={'class':'form-control', 'placeholder' : _('E-Mail')}),
            'username' : forms.TextInput(attrs={'class':'form-control', 'placeholder' : _('Username')}),
            'password1' : forms.PasswordInput(attrs={'class':'form-control'}),
            'password2' : forms.PasswordInput(attrs={'class':'form-control'}),
}
		model = User

class LoginForm(forms.Form):
    username = forms.CharField(
								required = True,
								label = '',
								widget = forms.TextInput(attrs = {
																	'class' : 'form-control',
																	'placeholder' : _('Username')
																 }
														)
							  )
    password = forms.CharField(
								required = True,
								label = '',
								widget=forms.PasswordInput(attrs = {
																	'class' : 'form-control',
																	'placeholder' : _('Password')
																    }
														  )
							  )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if not username or not password:
            return self.cleaned_data

        user = authenticate(username=username,
                            password=password)

        if user:
            self.user = user
        else:
            raise ValidationError(_("Wrong username or password!"))

        return self.cleaned_data
