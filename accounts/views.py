from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import City, State, Profile


def user_login(request):
    """ User authorization function """
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(request,
                                username=cd['login'],
                                password=cd['password'])
            remember = cd['remember']
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if not remember:
                        request.session.set_expiry(0)
                    return redirect('profile')
                else:
                    messages.warning(request, 'Ваш аккаунт был отключен')
            else:
                messages.error(request, 'Вы ввели неправильный логин или пароль')
    else:
        login_form = forms.LoginForm()
    return render(request, 'registration/login.html', {'login_form': login_form})


@login_required
def user_profile(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        city_form = forms.CityForm(data=request.POST)
        profile_form = forms.ProfileForm(data=request.POST, instance=profile,
                                         files=request.FILES)
        password_change_form = forms.PasswordChangeForm(data=request.POST,
                                                        request=request)
        if city_form.is_valid() and profile_form.is_valid() \
                and password_change_form.is_valid():
            cf = city_form.cleaned_data
            city, created = City.objects.get_or_create(
                osm_id=cf['state']['osm_id'],
            )
            if created:
                city.osm_type = cf['state']['osm_type']
                city.city = cf['state']['address']['city']
                city.display_name = cf['state']['display_name']
                city.lat = cf['state']['lat']
                city.lon = cf['state']['lon']
                city.boundingbox = str(cf['state']['boundingbox'])
                if cf.get('state').get('address').get('state'):
                    state, state_created = State.objects.get_or_create(
                        state=cf['state']['address']['state'])
                    city.state = state
                city.save()
            pr = profile_form.save(commit=False)
            pr.city = city
            pr.address = cf.get('address_json').get('display_name')
            pr.address_type = cf.get('address_json').get('osm_type')
            pr.address_id = cf.get('address_json').get('osm_id')
            pr.boundingbox = cf.get('address_json').get('boundingbox')
            pr.lat = cf.get('address_json').get('lat')
            pr.lon = cf.get('address_json').get('lon')
            profile_form.save(commit=True)
            cd = password_change_form.cleaned_data
            if cd['password']:
                user.set_password(cd['password'])
                user.save()
                re_user = authenticate(request,
                                       username=user.email,
                                       password=cd['password'])
                login(request, re_user)
            if password_change_form.has_changed() or profile_form.has_changed() or city_form.has_changed():
                messages.info(request, 'Ваши данные успешно обновлены')
            return redirect('profile')
        else:
            messages.error(request, 'Исправьте, пожалуйста, ошибки формы')
    else:
        profile_form = forms.ProfileForm(instance=profile)
        password_change_form = forms.PasswordChangeForm(request=request)
        city_form = forms.CityForm(initial={'city': profile.city.display_name,
                                            'geo_id': profile.city.osm_id,
                                            'address_id': profile.address_id,
                                            'address': profile.address})
    context = {
        'section': 'profile',
        'profile_form': profile_form,
        'city_form': city_form,
        'password_change_form': password_change_form,
    }
    return render(request, 'account/profile.html', context)
