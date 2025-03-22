from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

from django.db import models

#lab6 1
class CustomUser(AbstractUser):
    
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Număr de telefon")
    address = models.TextField(blank=True, null=True, verbose_name="Adresă")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Data nașterii")
    is_verified = models.BooleanField(default=False, verbose_name="Cont verificat")
    account_type = models.CharField(
        max_length=10,
        choices=[
            ('buyer', 'Cumpărător'),
            ('seller', 'Vânzător'),
        ],
        default='buyer',
        verbose_name="Tip de cont"
    )
    favorite_category = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Categorie preferată",
        help_text="Exemplu: Electronice, Modă, Alimente, etc."
    )
    #lab7
    cod = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cod de confirmare")
    email_confirmat = models.BooleanField(default=False, verbose_name="E-mail confirmat")
    def __str__(self):
        return f"{self.username} ({self.email})"

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name="products")
    tags = models.ManyToManyField('Tag', blank=True, related_name="products")  # Relatie Many-to-Many directă
    
    class Meta:
        permissions = [
            ('can_add_product', 'Poate adăuga produse'),
        ]


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField(max_length=255)
    is_primary = models.BooleanField(default=False)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)



