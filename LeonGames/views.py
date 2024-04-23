from django.views.generic import View, TemplateView, RedirectView, DetailView, ListView, FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LogoutView, LoginView
import decimal
import json
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Count, Sum, Avg, F
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy, reverse
from django.forms import formset_factory
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from .models import Venta, Marca, Juego, Comentarios_juegos, Pedido, Pedido_juego
from .forms import (FormJuego, FormRegistro, FormBuscarJuego, FormVenta)

#Página de bienvenida
class WelcomeView(ListView):
    model = Juego
    context_object_name = 'juegos'
    template_name = 'LeonGames/index.html'
    form_class = FormBuscarJuego

    def get_queryset(self):
        return Juego.objects.all()

    def get_queryset(self):
        juegos = super().get_queryset()
        form = self.form_class(self.request.GET)

        if form.is_valid():
            texto_busqueda = form.cleaned_data['texto']
            marcas_seleccionadas = form.cleaned_data['marca']

            juegos = juegos.filter(Titulo__contains=texto_busqueda)

            if len(marcas_seleccionadas) != 0:
                juegos = juegos.filter(Marca__in=marcas_seleccionadas)

        return juegos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        return context

class JuegosView(LoginRequiredMixin, ListView):
        model = Juego
        template_name = 'LeonGames/Juegos.html'
        context_object_name = 'juegos'
        login_url = '/logIn/'

        def get_queryset(self):
            return Juego.objects.all()


class AñadirJuegoView(LoginRequiredMixin, CreateView):
    model = Juego
    template_name = 'LeonGames/AñadirJuegos.html'
    form_class = FormJuego
    login_url = '/logIn/'

    def get_success_url(self):
        return '/juegos/'

    def form_valid(self, form):
        juego = form.save(commit=False)
        juego.save()
        return super().form_valid(form)


class EditarJuegoView(LoginRequiredMixin, UpdateView):
    model = Juego
    form_class = FormJuego
    template_name = 'LeonGames/editarJuego.html'
    login_url = '/logIn/'

    def form_valid(self, form):
        juego = form.save(commit=False)
        juego.save()
        return redirect('juegos')


class EliminarJuegoView(LoginRequiredMixin, DeleteView):
    model = Juego
    template_name = 'LeonGames/eliminarJuego.html'
    context_object_name = 'juego'
    login_url = '/logIn/'

    def get_object(self, queryset=None):
        return get_object_or_404(Juego, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['juego'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse('juegos')


class RegistroView(CreateView):
    template_name = 'LeonGames/registro.html'
    form_class = FormRegistro
    success_url = reverse_lazy('welcome')

    def form_valid(self, form):
        response = super().form_valid(form)

        user = form.save(commit=False)
        user.save()

        login(self.request, user)

        return response



class LogInView(LoginView):
    template_name = 'LeonGames/login.html'
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)

        next_ruta = self.request.GET.get('next')
        if next_ruta:
            return redirect(next_ruta)
        if next_ruta is None:
            next_ruta = '/'
            return redirect(next_ruta)
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)



class LogOutView(LogoutView):
    def dispatch(self, request):
        logout(self.request)
        return redirect(reverse_lazy('welcome'))


class VentasView(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'LeonGames/ventas.html'
    context_object_name = 'ventas'
    login_url = '/logIn/'


class CrearVenta(LoginRequiredMixin, CreateView):
    model = Venta
    form_class = FormVenta
    template_name = 'LeonGames/nuevaVenta.html'
    success_url = reverse_lazy('ventas')
    login_url = '/logIn/'

    def get_initial(self):
        initial = super().get_initial()
        initial['Fecha'] = timezone.now().date()
        initial['Vendedor'] = self.request.user
        return initial


class EditarVentaView(LoginRequiredMixin, UpdateView):
    model = Venta
    form_class = FormVenta
    template_name = 'LeonGames/editarVenta.html'
    login_url = '/logIn/'

    def get_success_url(self):
        return reverse_lazy('ventas')

    def form_valid(self, form):
        form.instance.Fecha = timezone.now().date()
        return super().form_valid(form)

    def get_queryset(self):
        return super().get_queryset().filter(Vendedor=self.request.user)


class EliminarVentaView(LoginRequiredMixin, DeleteView):
    model = Venta
    template_name = 'LeonGames/eliminarVenta.html'
    success_url = reverse_lazy('ventas')
    login_url = '/logIn/'

    def get_queryset(self):
        return super().get_queryset().filter(Vendedor=self.request.user)




