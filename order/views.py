from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from Book.models import Category
from home.models import Setting
from order.models import ShopCartForm, ShopCart


def index(request):
    return HttpResponse("Order App")

@login_required(login_url='/login') # Check Login
def addtocart(request,id):
    url = request.META.get('HTTP_REFERER') # get last url
    current_user = request.user #Access User Session Information

    ##########ÜRÜN SEPETTE VAR MI KONTROLÜ###########
    checkbook = ShopCart.objects.filter(book_id=id)
    if checkbook:
        control = 1   #ürün sepette var
    else:
        control = 0   #ürün sepette yok

    if request.method == 'POST':  #form post edildiyse   ÜRÜN SAYFASINDAN SEPETE EKLENDİYSE
        form = ShopCartForm(request.POST)
        if form.is_valid():

            if control == 1: #ürün varsa güncelle

                data = ShopCart.objects.get(book_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:  #ürün yoksa ekle

                data = ShopCart()  #model ile bağlantı kur
                data.user_id = current_user.id
                data.book_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()  #veritabanına kaydet

        messages.success(request, "Kitap sepete eklendi.")
        return HttpResponseRedirect(url)


    else:    #ÜRÜN ANASAYFADAN SEPETE EKLENDİYSE
        if control == 1:  # ürün varsa güncelle

            data = ShopCart.objects.get(book_id=id)
            data.quantity += 1
            data.save()

        else:  # ürün yoksa ekle

            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.book_id = id
            data.quantity = 1
            data.save()  # veritabanına kaydet

        messages.success(request, "Kitap sepete eklendi.")
        return HttpResponseRedirect(url)

    messages.warning(request, "Bir şeyler ters gitti!")
    return HttpResponseRedirect(url)

@login_required(login_url='/login') #Check Login
def shopcart(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in schopcart:
        total += rs.book.price * rs.quantity

    context = {
        'setting': setting,
        'page': 'shopcart',
        'schopcart': schopcart,
        'category': category,
        'total': total,
    }

    return render(request, 'Shopcart_books.html', context)

@login_required(login_url='/login') #Check Login
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Kitap sepetten silindi.")
    return HttpResponseRedirect('/shopcart/')