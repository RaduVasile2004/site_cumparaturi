from django import forms
from datetime import date
import re
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from .models import Product, Supplier, Category, Tag

#lab6 2
class CustomUserCreationForm(UserCreationForm):
    
    phone_number = forms.CharField(max_length=15, required=False, label="Număr de telefon")
    address = forms.CharField(widget=forms.Textarea, required=False, label="Adresă")
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2025)), required=False, label="Data nașterii")
    is_verified = forms.BooleanField(required=False, label="Cont verificat")
    account_type = forms.ChoiceField(choices=[('buyer', 'Cumpărător'), ('seller', 'Vânzător')], initial='buyer', label="Tip de cont")
    favorite_category = forms.CharField(max_length=50, required=False, label="Categoria favorită")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'address', 'birth_date', 'account_type', 'favorite_category', 'password1', 'password2']

#lab5 t1
class ProductFilterForm(forms.Form):
    name = forms.CharField(required=False, label='Name')
    description = forms.CharField(required=False, label="Description")
    min_price = forms.DecimalField(required=False, label='Minimum Price', min_value=0)
    max_price = forms.DecimalField(required=False, label='Maximum Price', min_value=0)
    stock = forms.DecimalField(required=False, label="Stock")
    category = forms.CharField(required=False, label="Category")
    supplier = forms.CharField(required=False, label="Supplier")
    tags = forms.CharField(required=False, label="Tags")

#lab5 t2
class ContactForm(forms.Form):
    alegeri = [
        ('1', 'reclamatie'),
        ('2', 'intrebare'),
        ('3', 'review'),
        ('4', 'cerere'),
        ('5', 'programare'),
    ]
    name = forms.CharField(required=True, label="Last Name", max_length=10)
    prenume = forms.CharField(required=False, label="First Name")
    data_nastere = forms.DateField(required=False, label="Date of birth", widget=forms.DateInput(attrs={'type': 'date'}))
    email = forms.EmailField(required=True, label="Email")
    conf_email = forms.EmailField(required=True, label="Confirmare Email")
    tip_mesaj = forms.MultipleChoiceField(choices=alegeri,widget=forms.CheckboxSelectMultiple, label="Tip mesaj", required=False)
    subiect = forms.CharField(required=True, label="Subiect")
    min_zile_asteptare = forms.IntegerField(required=False, min_value=1, label="Minim zile de asteptare")
    mesaj = forms.CharField(required=True, label="Mesaj")
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirmare_email = cleaned_data.get('conf_email')
        data_nasterii = cleaned_data.get('data_nastere')
        mesaj = cleaned_data.get('mesaj')
        nume = cleaned_data.get('name')

        
        if email and confirmare_email and email != confirmare_email:
            raise forms.ValidationError("E-mailul și confirmarea e-mailului trebuie să coincidă.")

        
        if data_nasterii:
            today = date.today()
            age = today.year - data_nasterii.year - ((today.month, today.day) < (data_nasterii.month, data_nasterii.day))
            if age < 18:
                raise forms.ValidationError("Expeditorul trebuie să fie major (18+).")

     
        if mesaj:
            words = re.findall(r'\w+', mesaj)
            if len(words) < 5 or len(words) > 100:
                raise forms.ValidationError("Mesajul trebuie să conțină între 5 și 100 cuvinte.")

            
            if any(word.startswith(('http://', 'https://')) for word in words):
                raise forms.ValidationError("Mesajul nu poate conține linkuri.")

            
            if words[-1].lower() != nume.lower():
                raise forms.ValidationError("Ultimul cuvânt din mesaj trebuie să fie numele utilizatorului (semnătura).")

        return cleaned_data
    
    

#lab6 3
class CustomLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label="Ține-mă minte pentru o zi")

    class Meta:
        fields = ['username', 'password', 'remember_me']

#lab5 t3      
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'supplier', 'category', 'tags']
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple)
