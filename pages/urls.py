from django.urls import path
from . import views as page_views

app_name = 'pages'

urlpatterns = [
    path('', page_views.home, name='home')
]