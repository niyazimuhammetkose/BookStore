from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from Book.models import Category
from home.models import UserProfile, Setting


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