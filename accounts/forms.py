from django.forms import ModelForm
from accounts.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'status', 'note']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Добавьте комментарий к заказу'}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError('Количество должно быть больше нуля')
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        note = cleaned_data.get('note')
        
        if status == 'В работе' and not note:
            self.add_error('note', 'Для заказов в работе необходимо добавить комментарий')
        
        return cleaned_data

class CustomerProfile(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'profile_pic']
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': '+7 (999) 999-99-99'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            phone = phone.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
            if not phone.replace('+', '').isdigit():
                raise forms.ValidationError('Номер телефона должен содержать только цифры')
        return phone

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте имя пользователя'})
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@domain.com'}),
        help_text='Требуется для связи и восстановления пароля'
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте пароль'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email