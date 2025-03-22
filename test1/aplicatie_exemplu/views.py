from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from .forms import AuthenticationForm

#from .models import auth_group
import re
import logging

from .models import Product
from .forms import ProductFilterForm
from .forms import ContactForm

# Create your views here.

from django.http import HttpResponse
def index(request):
	return HttpResponse("Primul raspuns")

def mesaj(request):
    return HttpResponse("Bună ziua!")

logger = logging.getLogger('django')

suma = 0
cereri = 0
def ex1lab2(request, sir):
    global suma, cereri
    cereri += 1
    #print(sir)
    val1 = re.findall(r'\d+', sir)
    suma += int(val1[len(val1) - 1])
    #val1 = val1.group()
    #print(rezultat.group.)
    return HttpResponse(f"suma numere {suma} {cereri}")

def ex4lab1(request):
    val_a = request.GET.get("a", 0)
    val_b = request.GET.get("b", 0)
    return HttpResponse(f"{int(val_a)} + {int(val_b)} = {int(val_a) + int(val_b)}")

def ex2lab2(request):
    parametri = {key: request.GET.getlist(key) for key in request.GET.keys()}
    
  
    return render(request, "afiseaza_liste.html", {"parametri": parametri})

# def test(request):
#     id = auth_group.objects.all();
#     return(id);
   

def product_list(request):
    products = Product.objects.all()
    form = ProductFilterForm(request.GET)

    if form.is_valid():
        
        if form.cleaned_data.get('name'):
            products = products.filter(name__icontains=form.cleaned_data['name'])

       
        if form.cleaned_data.get('category'):
            products = products.filter(category__icontains=form.cleaned_data['category'])


        if form.cleaned_data.get('min_price') is not None:
            products = products.filter(price__gte=form.cleaned_data['min_price'])
        if form.cleaned_data.get('max_price') is not None:
            products = products.filter(price__lte=form.cleaned_data['max_price'])

       
        if form.cleaned_data.get('in_stock'):
            products = products.filter(stock__gt=0)

    return render(request, 'product_list.html', {'form': form, 'products': products})

#lab5 t2
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
           
            return render(request, 'contact_success.html', {'form': form.cleaned_data})
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

from .models import CustomUser
from .utils import trimite_email_confirmare
import uuid

#lab6 2
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.cod = uuid.uuid4().hex  
            user.save()
            logger.info(f"Utilizatorul {user.username} a fost înregistrat cu succes.")
            trimite_email_confirmare(user)  
            logger.debug(f"Codul unic de confirmare {user.cod} a fost trimis la utilizator.")
            return render(request, 'email_sent.html')  
        else:
            logger.warning("Formularul de înregistrare a utilizatorului nu a fost valid.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login

def confirma_mail(request, cod):
    user = get_object_or_404(CustomUser, cod=cod)
    user.email_confirmat = True
    user.cod = None  
    user.save()
    return HttpResponse("E-mailul a fost confirmat! Te poți loga acum.")


from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomLoginForm

#lab6
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if not user.email_confirmat:
                    logger.warning(f"Utilizatorul {user.username} încearcă să se logheze, dar nu a confirmat e-mailul.")
                    messages.error(request, 'Te rugăm să confirmi e-mailul înainte de a te loga.')
                else:
                    login(request, user)
                    logger.info(f"Utilizatorul {user.username} s-a autentificat cu succes.")
                    return redirect('profile')
            else:
                logger.error(f"Autentificare eșuată pentru utilizatorul {username}. Nume de utilizator sau parolă incorectă.")
                messages.error(request, 'Nume de utilizator sau parolă incorectă')
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})

#lab6
def logout_view(request):
    logout(request)
    return redirect('login')


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

#lab6
@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

#lab6
@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Parola a fost schimbată cu succes!')
            return redirect('profile')
        else:
            messages.error(request, 'Te rog să corectezi erorile de mai jos.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


#lab8 task1
from django.http import HttpResponseForbidden

def custom_403_error(request, exception=None):
    titlu = "Acces interzis"  
    mesaj_personalizat = "Nu aveți permisiunea de a accesa această resursă."

    return render(
        request,
        "403.html",
        {
            'titlu': titlu,
            'mesaj_personalizat': mesaj_personalizat
        }
    )
    
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render


def is_admin_or_403(user):
    if not user.is_staff:
        raise PermissionDenied 
    return True

@user_passes_test(is_admin_or_403)
def restricted_view(request):
    return render(request, 'restricted.html') 



#lab8 task2
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ProductForm


@login_required
@permission_required('aplicatie_exemplu.add_product', raise_exception=True)
def add_product(request):
    if not request.user.has_perm('aplicatie_exemplu.can_add_product'):
        return HttpResponseForbidden('Nu ai voie să adaugi produse')

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list') 
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

# views.py (protejarea formularului)
from django.http import HttpResponseForbidden
from django.shortcuts import render

def check_add_product_permission(request):
    if not request.user.has_perm('aplicatie_exemplu.add_product'):
        return HttpResponseForbidden(render(request, '403_template.html', {
            'titlu': 'Eroare adăugare produse',
            'mesaj_personalizat': 'Nu ai voie să adaugi produse',
        }))
    return render(request, 'add_product.html')
