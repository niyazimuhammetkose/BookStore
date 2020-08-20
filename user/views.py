from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from Book.models import Category
from home.models import UserProfile, Setting
from user.forms import UserUpdateForm, ProfileUpdateForm

def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user      # Access User Session Information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'setting': setting,
        'page': 'user_profile',
        'category': category,
        'profile': profile}
    return render(request, 'user_profile.html', context)

def user_update(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) #request.user is user session data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profil bilgileriniz başarıyla güncellendi!")
            return redirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile) # "userprofile" model -> OneToOneField relatinon with user
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            'setting': setting,
            'page': 'user_update'
        }
        return render(request, 'user_update.html', context)

def change_password(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, "Şifreniz başarıyla değiştirildi")
            return HttpResponseRedirect('/user')
        else:
            messages.warning(request, 'Lütfen girdiğiniz bilgileri kontrol edin!.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'form': form, 'category': category, 'setting': setting, 'page': 'change_password'})