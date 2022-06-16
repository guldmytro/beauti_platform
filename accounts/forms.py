from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(
        label='E-mail или номер телефона',
        label_suffix=False,
        widget=forms.TextInput(attrs={
            'placeholder': False,
            'class': 'popup__input'
        })
    )
    password = forms.CharField(
        label='Пароль',
        label_suffix=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': False,
            'class': 'popup__input'
        })
    )
    remember = forms.BooleanField(
        required=False,
        label='Запомнить меня',
        initial=True,
        label_suffix=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'remember'
        })
    )
