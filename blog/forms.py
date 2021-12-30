from django import forms
from .models import Contacto
from .models import Usuario
from django.contrib.auth.models import User

from string import Template
from django.utils.safestring import mark_safe
from django.forms import ImageField

class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        html =  Template("""<img src="$link"/>""")
        return mark_safe(html.substitute(link=value))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email','last_name')
        labels = {}
        labels['last_name'] = "Apellidos"
        labels['email'] = "Email"

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nombre', 'descripcion', 'web','imagen_referencial'
        )
    #photo = ImageField(widget=PictureWidget)

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = '__all__'
        exclude = ('estado',)

        widgets = {
            'nombre':forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese su nombre',
                }
            ),
            'apellidos':forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese su apellido',
                }
            ),
            'correo':forms.EmailInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese su correo electrónico',
                }
            ),
            'asunto':forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el asunto',
                }
            ),
            'mensaje':forms.Textarea(
                attrs = {
                    'class':'form-control',
                    'placeholder': 'Ingrese su mensaje',
                }
            ),
        }