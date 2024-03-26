from django.views.generic import View, TemplateView, RedirectView, DetailView, ListView, FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LogoutView, LoginView

#Página de bienvenida
class WelcomeView(TemplateView):
    template_name = 'LeonGames/index.html'