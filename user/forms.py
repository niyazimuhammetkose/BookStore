from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, FileInput, Select

from home.models import UserProfile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': TextInput(attrs={'class': 'input', 'placeholder': 'Kullanıcı Adı'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'Email'}),
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'Ad'}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'Soyad'}),
        }

CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir'),
]

# Profile update form allows users to update image
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'country', 'image')
        widgets = {
            'phone': TextInput(attrs={'class': 'input', 'placeholder': 'Telefon'}),
            'address': TextInput(attrs={'class': 'input', 'placeholder': 'Adres'}),
            'city': Select(attrs={'class': 'input', 'placeholder': 'Şehir'}, choices=CITY),
            'country': TextInput(attrs={'class': 'input', 'placeholder': 'Ülke'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'Resim'}),
        }