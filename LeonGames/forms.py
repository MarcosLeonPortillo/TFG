from django import forms
from django.forms import SelectDateWidget
from django.utils.translation import gettext_lazy as _
from .models import Venta, Marca, Juego, Comentarios_juegos, Pedido, Pedido_juego
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class FormJuego(forms.ModelForm):
     class Meta:
        model = Juego
        fields = ['Titulo', 'Genero', 'DescripcionJuego', 'Desarrollador', 'Marca', 'Lanzamiento']

class FormRegistro(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

class EditarPerfilForm(UserChangeForm):
    new_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        help_text="Si desea cambiar la contraseña, rellene este campo."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'new_password', 'first_name', 'last_name']

class FormVenta(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['Juego', 'Vendedor', 'Precio', 'Fecha', 'DescripcionVenta', 'Consola']
        widgets = {
            'Vendedor': forms.HiddenInput(),
            'Fecha': forms.HiddenInput(),
        }


class FormBuscarJuego(forms.Form):
    texto = forms.CharField(required=False, widget=forms.TextInput())
    marca = forms.ModelMultipleChoiceField(required=False, queryset=Marca.objects.all(),
                                           widget=forms.CheckboxSelectMultiple)


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['Fecha', 'Vendedor', 'Comprador', 'Juego', 'Precio', 'Consola']
        widgets = {
            'Fecha': forms.HiddenInput(),
            'Vendedor': forms.HiddenInput(),
            'Comprador': forms.HiddenInput(),
            'Juego': forms.HiddenInput(),
            'Precio': forms.HiddenInput(),
            'Consola': forms.HiddenInput(),
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentarios_juegos
        fields = ['Texto', 'Valoracion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Texto'].widget.attrs['required'] = 'required'