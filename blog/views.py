import random
from django.http.response import Http404, HttpResponse, HttpResponseRedirect

from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import ListView,DetailView, View
from .models import Post, Categoria, RedesSociales, Web, Usuario
from django.contrib.auth.models import User
from .forms import UserProfileForm, UserForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.defaults import page_not_found
from pprint import pprint
import logging


from .utils import *
# Create your views here.

class Login(View):
    def get(self, request):
        if request.user.is_authenticated():
            usr_id = request.session.get('_auth_user_id')
            user = User.objects.get(id=usr_id)
            profile_form = UserProfileForm(instance=user.usuario)
            user_form = UserForm(instance=user)
            return render(request, 'registration/profile.html', {
                'user_form': user_form,
                'profile_form': profile_form
            })           
        else:
            contexto = {}
            return render(request, 'registration/login.html', contexto) 

    def post(self, request):
        if request.method != 'POST':
            contexto = {
                'form':{
                  'errors':"Metodo no permitido"
                }
            }
            return render(request, 'registration/login.html', contexto)
        if request.user is not None and request.user.is_authenticated:
            usr_id = request.session.get('_auth_user_id')
            user = User.objects.get(id=usr_id)
            profile_form = UserProfileForm(instance=user.usuario)
            user_form = UserForm(instance=user)
            return render(request, 'registration/profile.html', {
                'user_form': user_form,
                'profile_form': profile_form
            })  
        try:
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            
            if user is not None:
              if user.is_active: 
                login(request, user)
                #pprint(user)
                #request.session['usuario'] = user
                #logging.debug(request.session['usuario'])
                #logging.info(request.session.get('_auth_user_id'))
                #return HttpResponseRedirect('/accounts/profile/')
                #user_form = UserForm(instance=request.user)

                profile_form = UserProfileForm(instance=user.usuario)
                user_form = UserForm(instance=user)

                return render(request, 'registration/profile.html', {
                    'user_form': user_form,
                    'profile_form': profile_form
                })
              else:
                contexto = {
                    'form':{
                    'errors':"Su usuario esta deshabilitado"
                    }
                }
                return render(request, 'registration/login.html', contexto)                  
            else:
              contexto = {
                  'form':{
                    'errors':"El usuario no existe"
                  }
              }
              return render(request, 'registration/login.html', contexto)
        except:
            contexto = {
                'form':{
                    'errors':"Error al intentar loguearse, por favor contacte a soporte."
                }
            }            #return HttpResponse("Login Error.")
            return render(request, 'registration/login.html', contexto)

class Profile(View):
    def get(self, request, *args, **kwargs):
        #pprint(request.session['usuario'])
        #logging.debug(request.session.get('usuario')
        usr_id = request.session.get('_auth_user_id')
        user = User.objects.get(id=usr_id)
        profile_form = UserProfileForm(instance=user)
        user_form = UserForm(instance=user.usuario)        
        contexto = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'registration/profile.html', contexto)
    def post(self, request, *args, **kwargs):
        #logging.debug(request.session['usuario'])
        #pprint(request.session['usuario'])
        usr_id = request.session.get('_auth_user_id')
        user = User.objects.get(id=usr_id)
        profile_form = UserProfileForm(instance=user.usuario)
        user_form = UserForm(instance=user)           
        contexto = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'registration/profile.html', contexto)

class Inicio(ListView):

    def get(self, request, *args, **kwargs):

        
        #obtengo solo los id de los posts publicados y estado = true
        posts = list(Post.objects.filter(
                estado = True,
                publicado = True
                ).values_list('id', flat = True))
      
        if len(posts) > 0:
            #elijo un post aleatorio
            principal = random.choice(posts)
            posts.remove(principal)
            principal = consulta(principal)

            post1 = random.choice(posts)
            posts.remove(post1)
            secundario = consulta(post1)


            post2 = random.choice(posts)
            posts.remove(post2)
            terciario = consulta(post2)

            #obtengo los ultimos 4 posts mas recientes 
            last_four_posts = Post.objects.filter(
                estado = True,
                publicado = True
            ).order_by('-fecha_publicacion')[:4]
    
            posts_cine = get_posts(nombre_categoria='Cine', cantidad=3)
            posts_musica =  get_posts(nombre_categoria='Música', cantidad=3)
            posts_fotografia =  get_posts(nombre_categoria='Fotografía', cantidad=3)
        

            # 5 posts aleatorios
            random_post = get_random_posts(5)
            usuario = Usuario.objects.get(id=1)

            contexto = {
                'principal' : principal,
                'secundario': secundario,
                'terciario': terciario,
                'posts_recientes': last_four_posts,
                'posts_cine': posts_cine,
                'posts_musica': posts_musica,
                'posts_fotografia': posts_fotografia,
                'random_posts': random_post,
                'sociales': get_redes(),
                'web': get_web(),
                'usuario':usuario,
            }
            
            return render(request, 'index.html', contexto)
        else:

            return render(request, 'vacio.html', {})

class DetallePost(DetailView):
    def get(self, request, id, *args, **kwargs):
#    def get(self, request, slug, *args, **kwargs):
        try:
            #post = Post.objects.get(slug = slug)
            post = Post.objects.get(id = id)
            usuario = Usuario.objects.get(id=post.usuario.id)
            posts = list(Post.objects.filter(
                estado = True,
                publicado = True
                ).values_list('id', flat = True))
            
      
                
        except:
            post = None
            usuario = None
            
        try:
            post_anterior = Post.objects.get(id=post.id - 1)
            post_posterior = Post.objects.get(id=post.id + 1)

        except:
            post_anterior = None
            post_posterior = None
           
        
        contexto = {
            'post' : post,
            'post_anterior': post_anterior,
            'post_posterior': post_posterior,
            'random_posts':  get_random_posts(5),
            'related_posts': get_posts(nombre_categoria=post.categoria.nombre, cantidad=3),
            'sociales' : get_redes(),
            'web' : get_web(),
            'usuario': usuario,
        }

        return render(request, 'blog-post.html', contexto)


class AcercaDe(DetailView):
    def get(self, request, *args, **kwargs):
        contexto = {
            'web' : get_web(),
            'sociales' : get_redes(),
        }
        return render(request, 'about.html', contexto)

class FormularioContacto(View):
    def get(self,request,*args,**kwargs):
       
        contexto = {
            'sociales':get_redes(),
            'web':get_web(),
        }
        return render(request,'contact.html',contexto)


class Listado(ListView):
    def get(self,request,nombre_categoria,*args,**kwargs):
        is_non_empty= bool(nombre_categoria)
        if(is_non_empty):    
          contexto = generarCategoria(request,nombre_categoria)
          return render(request,'category.html',contexto)
        else:
          contexto = generarCategoria(request,'todo')
          return render(request,'category.html',contexto)

class Search_Posts(ListView):
     def get(self,request,*args,**kwargs):
        query = request.GET.get("q")
        queryset_list = Post.objects.all()
        if query:
            queryset_list = queryset_list.filter(Q(titulo__icontains=query) | Q(descripcion__icontains=query) )
        paginator = Paginator(queryset_list, 4)
        pagina = request.GET.get('page')
        posts = paginator.get_page(pagina)
        contexto = {
        'posts':posts,
        'query':query,
        'sociales':get_redes(),
        'web':get_web(),
        }
        return render(request,'list_search.html',contexto)

def mi_error_404(request, exception):
    nombre_template = '404.html'
 
    return page_not_found(request, template_name=nombre_template)