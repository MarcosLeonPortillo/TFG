from django.urls import path
from .views import (WelcomeView)
#Ponemos la urls que llevan los datos al template
urlpatterns = [
path('', WelcomeView.as_view(), name='welcome'),
]