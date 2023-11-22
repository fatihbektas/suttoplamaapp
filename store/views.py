from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import json
import datetime
from suttoplamaapp.decorators import *


@login_required(login_url='account:login')
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False
        )
        cart_items = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        # Navbar sepetteki ürün miktarı
        cart_items = order['get_cart_items']

    products = Product.objects.all()
    context = {
        'products': products,
        'cart_items': cart_items,
    }
    return render(request, 'store/store.html', context=context)


@login_required(login_url='account:login')
def shopping_cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False
        )
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'store/shopping-cart.html', context=context)


@login_required(login_url='account:login')
def checkout(request):
    transaction_id = datetime.datetime.now().timestamp()
    customer = request.user.customer
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False
    )
    order.transaction_id = transaction_id
    form = OrderAddressForm(request.POST or None, instance=order)

    items = order.orderitem_set.all()
    cart_items = order.get_cart_items

    if form.is_valid():
        order = form.save(commit=False)
        order.complete = True
        order.save()
        return redirect('mainboard:user-page')

    context = {
        'form': form,
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'store/checkout.html', context=context)


@login_required(login_url='account:login')
def update_item(request):
    data = json.loads(request.body)

    product_id = data['product_id']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)

    order, created = Order.objects.get_or_create(
        customer=customer, complete=False
    )
    order_item,  created = OrderItem.objects.get_or_create(
        order=order, product=product
    )

    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Ürün eklendi.', safe=False)


@login_required(login_url='account:login')
def order_delete(request, id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, id=id)
        user_group = request.user.groups.all()[0].name
        if user_group == "customer" and not order.assign_date:
            order.delete()
            messages.success(request, "Siparişiniz silinmiştir.")
            return redirect('mainboard:user-page')
        elif user_group == "admin" and not order.assign_date:
            order.delete()
            messages.success(request, "Sipariş silinmiştir.")
            return redirect('mainboard:mainboard')
        else:
            messages.error(request, "Bu aşamada silme işlemi yapılamaz.")
            if user_group == "admin":
                return redirect('mainboard:mainboard')
            else:
                return redirect('mainboard:user-page')
    else:
        messages.error(request, "Silme işlemi için yetkili değilsiniz.")


@login_required(login_url='account:login')
def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    items = order.orderitem_set.all()
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'store/detail.html', context=context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def order_assign(request, id):
    if not request.user.has_perm('order.is_operator'):
        return Http404()
    order = get_object_or_404(Order, id=id)
    services = Service.objects.all()
    form = OrderAssignForm(request.POST or None)

    context = {
        'order': order,
        'services': services,
        'form': form,
    }
    return render(request, 'store/assign.html', context=context)


@login_required(login_url='account:login')
@allowed_users(allowed_roles=['admin'])
def order_assign_to_service(request, id, sid):
    order = get_object_or_404(Order, id=id)
    order.service = Service.objects.get(id=sid)
    order.assign_date = datetime.datetime.now()
    order.save()
    messages.success(request, 'Sipariş servis ekibine atandı.')
    return HttpResponseRedirect(order.get_absolute_url())


@login_required(login_url='account:login')
@allowed_users(allowed_roles=['service'])
def order_service(request, id):
    order = get_object_or_404(Order, id=id)
    order.service_date = datetime.datetime.now()

    secs = int((order.service_date.replace(tzinfo=None) -
               order.assign_date.replace(tzinfo=None)).seconds)
    order.service_time = secs // 3600
    order.status = 'Taşımada'
    order.save()
    messages.success(request, 'Ürün teslim alındı/taşımada.')
    return HttpResponseRedirect(order.get_absolute_url())


@login_required(login_url='account:login')
@allowed_users(allowed_roles=['service'])
def order_delivery(request, id):
    order = get_object_or_404(Order, id=id)
    order.delivery_date = datetime.datetime.now()
    secs = int((order.delivery_date.replace(tzinfo=None) -
               order.service_date.replace(tzinfo=None)).seconds)
    order.delivery_time = secs // 3600
    order.status = 'Teslim edildi'
    order.is_delivered = True
    order.save()
    messages.success(request, 'Ürün merkeze teslim edildi.')
    return HttpResponseRedirect(order.get_absolute_url())
