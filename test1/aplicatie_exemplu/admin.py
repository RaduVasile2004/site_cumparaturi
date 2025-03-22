from django.contrib import admin
from .models import Category
from .models import Supplier
from .models import Product
from .models import ProductImage
from .models import Tag
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm




# admin.site.register(CustomUser)
#lab4 task1
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Tag)

admin.site.site_header = "Panou de Administrare Site"
admin.site.site_title = "Admin Site"
admin.site.index_title = "Bine ai venit în panoul de administrare"

class CategoryAdmin(admin.ModelAdmin):
    list_filter = ("name", "description")
    
admin.site.register(Category, CategoryAdmin)

#lab4 task2
class CategoryFilter(admin.SimpleListFilter):
    title = 'Categoria'
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        return [(cat.id, cat.name) for cat in Category.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category_id=self.value())
        return queryset

class SupplierFilter(admin.SimpleListFilter):
    title = 'Furnizor'
    parameter_name = 'supplier'

    def lookups(self, request, model_admin):
        return [(sup.id, sup.name) for sup in Supplier.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(supplier_id=self.value())
        return queryset

class TagFilter(admin.SimpleListFilter):
    title = 'Etichete'
    parameter_name = 'tags'

    def lookups(self, request, model_admin):
        return [(tag.id, tag.name) for tag in Tag.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tags__id=self.value())
        return queryset

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'supplier', 'created_at')
    list_filter = (CategoryFilter, SupplierFilter, TagFilter, 'price', 'stock')
    search_fields = ('name', 'description')
    list_per_page = 10


if not admin.site.is_registered(Product):
    admin.site.register(Product, ProductAdmin)


#lab8 task2
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informații suplimentare', {
            'fields': (
                'phone_number', 
                'address', 
                'birth_date', 
                'is_verified', 
                'account_type', 
                'favorite_category',
                'cod',
                'email_confirmat'
            ),
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informații suplimentare', {
            'fields': (
                'phone_number', 
                'address', 
                'birth_date', 
                'is_verified', 
                'account_type', 
                'favorite_category',
            ),
        }),
    )
    list_display = ('username', 'email', 'is_staff', 'is_verified', 'account_type')
    list_filter = ('is_verified', 'account_type', 'is_staff')

if not admin.site.is_registered(CustomUser):
    admin.site.register(CustomUser, CustomUserAdmin)