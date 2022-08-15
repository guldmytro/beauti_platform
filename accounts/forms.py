from django import forms
from . import models as profile_models
import requests
from django.contrib.auth import get_user_model, authenticate

REQUIRED_SUFFIX = '*'
GEO_API = 'https://nominatim.openstreetmap.org/lookup'
headers = {
    'accept-language': 'ru-RU'
}
User = get_user_model()


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


class ProfileForm(forms.ModelForm):
    fullname = forms.CharField(label='ФИО', label_suffix=REQUIRED_SUFFIX,
                               widget=forms.TextInput(attrs={
                                   'class': 'popup__input'
                               }))
    phone = forms.CharField(label='Телефон', label_suffix=REQUIRED_SUFFIX,
                            widget=forms.TextInput(attrs={
                                'type': 'tel',
                                'class': 'popup__input'
                            }))
    photo = forms.ImageField(label='', label_suffix='')

    class Meta:
        model = profile_models.Profile
        fields = ('fullname', 'phone', 'photo',)


class CityForm(forms.Form):
    geo_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    city = forms.CharField(label='Город', label_suffix=REQUIRED_SUFFIX,
                           widget=forms.TextInput(attrs={
                               'class': 'popup__input'
                           }))
    address_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    address = forms.CharField(label='Адрес', label_suffix=REQUIRED_SUFFIX,
                              widget=forms.TextInput(attrs={
                                  'class': 'popup__input',
                                  'autocomplete': 'off'
                              }))

    def clean_city(self):
        cd = self.cleaned_data
        geo_id = cd['geo_id']
        if len(geo_id) == 0:
            raise forms.ValidationError('Пожалуйста, выберите город из \
                        выпадающего списка во вложении')
        city_detail = requests.get(f'{GEO_API}?osm_ids=R{geo_id}&format=json',
                                   headers).json()
        if len(city_detail) == 0:
            raise forms.ValidationError('Пожалуйста, выберите город из \
            выпадающего списка')
        cd['state'] = city_detail[0]
        return cd['city']

    def clean_address(self):
        cd = self.cleaned_data
        address_id = cd['address_id']
        if len(address_id) == 0:
            raise forms.ValidationError('Пожалуйста, выберите адрес из \
                                        выпадающего списка')
        address_detail = requests.get(f'{GEO_API}?osm_ids=W{address_id}&format=json',
                                      headers).json()
        if len(address_detail) == 0:
            raise forms.ValidationError('Пожалуйста, выберите адрес из \
                                        выпадающего списка')
        cd['address_json'] = address_detail[0]
        return cd['address']

    class Meta:
        fields = ('geo_id', 'city', 'address_id', 'address')


class UserForm(forms.ModelForm):
    email = forms.EmailField(label='E-mail', label_suffix=REQUIRED_SUFFIX,
                             widget=forms.EmailInput(attrs={
                                 'class': 'popup__input'
                             }))

    def clean_email(self):
        cd = self.cleaned_data

    class Meta:
        model = User
        fields = ('email',)


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='Старый пароль',
                                   required=False,
                                   widget=forms.PasswordInput(attrs={
                                       'placeholder': False,
                                       'autocomplete': 'off',
                                       'class': 'popup__input'
                                   }))
    password = forms.CharField(label='Пароль',
                               min_length=8,
                               required=False,
                               help_text='Пароль должен содержать как минимум 8 символов',
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': False,
                                   'autocomplete': 'off',
                                   'class': 'popup__input'
                               }))
    password2 = forms.CharField(label='Повторите пароль',
                                min_length=8,
                                required=False,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': False,
                                    'autocomplete': 'off',
                                    'class': 'popup__input'
                                }))

    def __init__(self, *args, **kwargs):
        """Passing request into form"""
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        if len(cd['password2']) < 8 and len(cd['password2']) > 1:
            raise forms.ValidationError('Минимальная длина пароля должна быть не меньше 8 символов')
        return cd['password2']

    def clean(self):
        user = self.request.user
        cd = self.cleaned_data
        if len(cd['old_password']) > 0:
            check_user = authenticate(self.request,
                                      username=user.username,
                                      password=cd['old_password'])
            if check_user is not None:
                if len(cd['password']) < 8:
                    self.add_error('password', 'Длина нового пароля должна быть не меньше 8 символов')
            else:
                self.add_error('old_password', 'Неправильный пароль')
