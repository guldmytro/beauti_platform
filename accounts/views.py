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
        profile_form = forms.ProfileForm(data=request.POST, instance=profile)
        user_form = forms.UserForm(data=request.POST, instance=user)
        if city_form.is_valid() and profile_form.is_valid() \
                and user_form.is_valid():
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
            profile_form.save(commit=True)
            user_form.save(commit=True)
    else:
        profile_form = forms.ProfileForm(instance=profile)
        city_form = forms.CityForm(initial={'city': profile.city.display_name,
                                            'geo_id': profile.city.osm_id})
        user_form = forms.UserForm(instance=user)
    context = {
        'section': 'profile',
        'profile_form': profile_form,
        'city_form': city_form,
        'user_form': user_form
    }
    return render(request, 'account/profile.html', context)
