from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
# Create your views here.
from Book.models import Book, Category, Images, Comment
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactForm, ContactFormMessage, UserProfile
from order.models import ShopCart

def index (request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    sliderdata = Book.objects.all()[:4]
    latestdata = Book.objects.all().order_by('-id')[:4]
    randomdata = Book.objects.all().order_by('?')[:8]
    bestrateddata = Book.objects.all()[:4]
    category = Category.objects.all()
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # count item in shop cart
    context = {'setting': setting,
               'page': 'home',
               'sliderdata': sliderdata,
               'category': category,
               'latestdata': latestdata,
               'randomdata': randomdata,
               'bestrateddata': bestrateddata}
    return render(request, 'index.html', context)

def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'page': 'aboutus', 'category': category}
    return render(request, 'aboutus.html', context)

def contact(request):
    if request.method == 'POST':   # form post edildiyse
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # model ile bağlantı kur
            data.name = form.cleaned_data['name']  # formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veritabanına kaydet
            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkür ederiz")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    form = ContactForm()
    context = {'setting': setting, 'page': 'contact', 'form': form, 'category': category}
    return render(request, 'contact.html', context)

def references(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'page': 'references', 'category': category}
    return render(request, 'references.html', context)

def category_books(request,id,slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    books = Book.objects.filter(category_id=id)
    context = {
        'setting': setting,
        'books': books,
        'page': 'books',
        'category': category,
        'categorydata': categorydata
    }
    return render(request, 'books.html', context)

def book_details(request, id ,slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    book = Book.objects.get(pk=id)
    images = Images.objects.filter(book_id=id)
    comments = Comment.objects.filter(book_id=id, status='True')
    context = {
        'setting': setting,
        'page': 'book_details',
        'book': book,
        'category': category,
        'images': images,
        'comments': comments,
    }
    return render(request, 'book_details.html', context)

def book_search(request):
    if request.method == 'POST':     # form post edildiyse
        form = SearchForm(request.POST)
        if form.is_valid():
            setting = Setting.objects.get(pk=1)
            category = Category.objects.all()
            query = form.cleaned_data['query']     # formdan bilgiyi al
            books = Book.objects.filter(title__icontains=query)   # Select * from Book where title like %query%
            context = {
                'setting': setting,
                'page': 'book_search',
                'books': books,
                       'category': category,
            }
            return render(request, 'book_search.html', context)

    return HttpResponseRedirect('/')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #Redirect to a success page
            messages.success(request, "Hoş Geldiniz..")
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Giriş Hatası! Kullanıcı adı ya da şifre yanlış")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {
        'setting': setting,
        'page': 'login',
        'category': category,
    }
    return render(request, 'login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            # create data in profile table for user
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.save()
            messages.success(request, "Hoş geldiniz..")
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {
        'setting': setting,
        'page': 'signup',
        'category': category,
        'form': form,
    }

    return render(request, 'signup.html', context)