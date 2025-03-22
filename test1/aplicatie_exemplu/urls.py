from django.urls import path
from . import views
from .views import product_list
from .views import contact_view
from .views import register_view
from .views import login_view
from .views import logout_view
from .views import profile_view
from .views import change_password_view
from .views import confirma_mail
from .views import restricted_view

from django.conf.urls import handler403
handler403 = 'django.views.defaults.permission_denied'

urlpatterns = [
	path("", views.index, name="index"),
    path("mesaj/", views.mesaj, name="mesaj"),
    path("pag/<str:sir>", views.ex1lab2, name = "ex1lab2"),
    path("ex4lab1", views.ex4lab1, name = "ex4lab1"),
    path("liste/", views.ex2lab2, name = "ex2lab2"),
    path('products/', product_list, name='product_list'),
    path('contact/', contact_view, name='contact'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('change_password/', change_password_view, name='change_password'),
    path('confirma_mail/<str:cod>/', confirma_mail, name='confirma_mail'),
    path('restricted/', views.restricted_view, name='restricted'),
    path('add_product/', views.add_product, name='add_product'),
]

