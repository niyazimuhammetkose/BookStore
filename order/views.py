from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from Book.models import Category, Book
from home.models import Setting, UserProfile
from order.models import ShopCartForm, ShopCart, OrderForm, Order, OrderBook


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

        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # count item in shop cart
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

        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # count item in shop cart
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
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # count item in shop cart
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
    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # count item in shop cart
    messages.success(request, "Kitap sepetten silindi.")
    return HttpResponseRedirect('/shopcart/')

@login_required(login_url='/login') #check login
def orderbook(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in schopcart:
        total += rs.book.price * rs.quantity

    if request.method == 'POST': #if there is a post
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name'] #get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.country = form.cleaned_data['country']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()

            #move shopcart items to order book items
            schopcart = ShopCart.objects.filter(user_id = current_user.id)
            for rs in schopcart:
                    detail = OrderBook()
                    detail.order_id = data.id #Order ID
                    detail.book_id = rs.book_id
                    detail.user_id = current_user.id
                    detail.quantity = rs.quantity
                    detail.price = rs.book.price
                    detail.amount = rs.amount
                    detail.save()
                    #Reduce quantity of sold  book from Amount Of Book
                    book = Book.objects.get(id=rs.book_id)
                    book.amount -=rs.quantity
                    book.save()
                    #*************************************

            ShopCart.objects.filter(user_id=current_user.id).delete() #Clear & Delete  shopcart
            request.session['cart_items'] = 0
            messages.success(request, "Siparişiniz alındı. Teşekkürler")
            return render(request, 'Order_Compeleted.html', {'ordercode': ordercode, 'category': category, 'setting': setting, 'page': 'order_completed'})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderbook/")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'schopcart': schopcart,
               'category': category,
               'total': total,
               'form': form,
               'profile': profile,
               'setting': setting,
               'page': 'order_form'
               }

    return render(request, 'Order_Form.html', context)