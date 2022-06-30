from django import forms
from . import models as profile_models
import requests
from django.contrib.auth import get_user_model

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


    class Meta:
        model = profile_models.Profile
        fields = ('fullname', 'phone',)


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

    class Meta:
        model = User
        fields = ('email',)
