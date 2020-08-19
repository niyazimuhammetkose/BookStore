from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from Book.models import Book, Category, Images
from home.models import Setting, ContactForm, ContactFormMessage


def index (request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Book.objects.all()[:4]
    latestdata = Book.objects.all().order_by('-id')[:4]
    randomdata = Book.objects.all().order_by('?')[:8]
    bestrateddata = Book.objects.all()[:4]
    category = Category.objects.all()
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
    context = {
        'setting': setting,
        'page': 'book_details',
        'book': book,
        'category': category,
        'images': images,
    }
    return render(request, 'book_details.html', context)