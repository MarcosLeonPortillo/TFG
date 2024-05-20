from django.views.decorators.csrf import csrf_exempt
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
from .forms import (FormJuego, FormRegistro, FormBuscarJuego, FormVenta, EditarPerfilForm,
PedidoForm, ComentarioForm)

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

    def get_queryset(self):
        # Filtrar las ventas del usuario logeado
        return Venta.objects.filter(Vendedor=self.request.user)


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


class PerfilUsuarioView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'LeonGames/perfil.html'


    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Obtener el historial de pedidos del usuario
        historial_pedidos = Pedido.objects.filter(Comprador=user)
        context['historial_pedidos'] = historial_pedidos
        return context


class EditarPerfilView(LoginRequiredMixin, UpdateView):
    form_class = EditarPerfilForm
    template_name = 'LeonGames/editarPerfil.html'
    login_url = '/logIn/'

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def get_success_url(self):
        return reverse_lazy('perfil')

    def form_valid(self, form):
        user = self.request.user
        new_password = form.cleaned_data.get('password')  # Cambiado de 'new_password' a 'password'
        if new_password:
            user.set_password(new_password)
            user.save()
        return super().form_valid(form)


class DetalleJuegoView(LoginRequiredMixin, DetailView):
    model = Juego
    template_name = 'LeonGames/detalleJuego.html'
    context_object_name = 'juego'
    login_url = '/logIn/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        juego = self.get_object()

        # Obtener las ventas relacionadas al juego excluyendo las del usuario actual
        ventas_relacionadas = Venta.objects.filter(Juego=juego).exclude(Vendedor=self.request.user)
        context['ventas_relacionadas'] = ventas_relacionadas

        # Obtener los comentarios del juego
        comentarios = Comentarios_juegos.objects.filter(Juego=juego)
        context['comentarios'] = comentarios

        # Verificar si el usuario ha realizado un pedido y/o un comentario
        user = self.request.user
        if user.is_authenticated:
            pedido_realizado = Pedido.objects.filter(Juego=juego, Comprador=user).exists()
            comentario_realizado = Comentarios_juegos.objects.filter(Juego=juego, Usuario=user).exists()
            context['pedido_realizado'] = pedido_realizado
            context['comentario_realizado'] = comentario_realizado

        # Calcular el precio medio de las ventas del juego
        precio_medio_ventas = Venta.objects.all().aggregate(precio_medio=Avg('Precio'))
        context['precio_medio_ventas'] = precio_medio_ventas['precio_medio']

        return context


class ComprarVentaView(LoginRequiredMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    success_url = reverse_lazy('welcome')
    template_name = "LeonGames/comprarVenta.html"
    login_url = '/logIn/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venta_id = self.kwargs.get('venta_id')
        venta = get_object_or_404(Venta, pk=venta_id)
        context['venta'] = venta
        context['juego'] = venta.Juego
        context['precio'] = venta.Precio
        context['consola'] = venta.Consola
        return context

    @csrf_exempt
    def form_valid(self, form):
        form.instance.Fecha = timezone.now().date()
        form.instance.Comprador = self.request.user
        venta_id = self.kwargs.get('venta_id')
        venta = get_object_or_404(Venta, pk=venta_id)
        form.instance.Vendedor = venta.Vendedor
        form.instance.Juego = venta.Juego
        form.instance.Precio = venta.Precio
        form.instance.Consola = venta.Consola
        return super().form_valid(form)


@csrf_exempt
def procesar_pedido(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        venta_id = data.get('venta_id')

        try:
            venta = Venta.objects.get(pk=venta_id)
        except Venta.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Venta no encontrada'})

        comprador = request.user
        Pedido.objects.create(
            Fecha=timezone.now().date(),
            Comprador=comprador,
            Vendedor=venta.Vendedor,
            Juego=venta.Juego,
            Precio=venta.Precio,
            Consola=venta.Consola
        )

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'fail', 'message': 'Método no permitido'})


class CrearComentarioView(LoginRequiredMixin, CreateView):
    model = Comentarios_juegos
    form_class = ComentarioForm
    template_name = 'LeonGames/crearComentario.html'
    login_url = '/logIn/'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el juego relacionado con el comentario
        context['juego'] = Juego.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.Usuario = self.request.user
        # Obtener la instancia del juego correspondiente al ID proporcionado
        juego = get_object_or_404(Juego, pk=self.kwargs['pk'])
        form.instance.Juego = juego
        return super().form_valid(form)

    def get_success_url(self):
        juego_id = self.kwargs['pk']
        return reverse('detalleJuego', kwargs={'pk': juego_id})



class EditarComentarioView(LoginRequiredMixin, UpdateView):
    model = Comentarios_juegos
    form_class = ComentarioForm
    template_name = 'LeonGames/editarComentario.html'
    login_url = '/logIn/'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(Usuario=self.request.user)

    def form_valid(self, form):
        form.instance.Usuario = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        juego = get_object_or_404(Juego, pk=self.object.Juego.pk)
        context['juego'] = juego
        return context

    def get_success_url(self):
        return reverse_lazy('detalleJuego', kwargs={'pk': self.object.Juego.pk})


class EliminarComentarioView(LoginRequiredMixin, DeleteView):
    model = Comentarios_juegos
    template_name = 'LeonGames/eliminarComentario.html'
    login_url = '/logIn/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comentario = self.object
        context['comentario'] = comentario
        return context

    def get_success_url(self):
        juego_pk = self.object.Juego.pk
        return reverse_lazy('detalleJuego', kwargs={'pk': juego_pk})