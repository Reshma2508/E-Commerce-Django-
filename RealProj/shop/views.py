from django.shortcuts import render, redirect
from .models import Product , Cart,Order

from .models import Customer
from django.core.paginator import Paginator
from .forms import cform , SignupForm
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
# Create your views here.

def index(r):
    product_objects = Product.objects.all()

    # search code
    item_name = r.GET.get('item_name')
    if item_name != '' and item_name is not None:
        product_objects = product_objects.filter(title__icontains=item_name)

    # paginator code
    paginator = Paginator(product_objects, 4)
    page = r.GET.get('page')
    product_objects = paginator.get_page(page)

    return render(r, 'shop/index.html', {'product_objects': product_objects})


def register(r):
    form = cform()
    if r.method == 'POST':
        form = cform(r.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('accounts/login')

    return render(r, 'shop/register.html', {'form': form})

@login_required
def details(request, id):
    product_object = Product.objects.get(id=id)
    return render(request, 'shop/detail.html', {'product_object': product_object})


def signup(r):

    form=SignupForm()
    if r.method=='POST':
        form=SignupForm(r.POST)
        if form.is_valid():
            user1=form.save()
            user1.set_password(user1.password)
            user1.save()
            return HttpResponseRedirect('/accounts/login')
    return render(r,'shop/signup.html',{'form':form})



def user_detail(r,id):
    product_object = Product.objects.get(id=id)
    return render(r,'shop/user_details.html',{'product_object': product_object})


@login_required
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, id):
    product = Product.objects.get(id=id)
    try:
        cart_item = Cart.objects.get(user=request.user, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except Cart.DoesNotExist:
        pass
    return redirect('cart')

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.discount_price * item.quantity for item in cart_items)
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})



def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.discount_price * item.quantity for item in cart_items)
    if request.method == "POST":
        items = request.POST.get('items', '')
        name = request.POST.get('name', "")
        email = request.POST.get('email', "")
        address = request.POST.get('address', "")
        city = request.POST.get('city', "")
        state = request.POST.get('state', "")
        zipcode = request.POST.get('zipcode', "")
        total = request.POST.get('total', "")
        order = Order(items=items, name=name, email=email, address=address, city=city, state=state, zipcode=zipcode,
                      total=total)
        order.save()

    return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total_price': total_price})
