from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from store.models import Order


def store(request):
    return render(request, 'store/store.html')


def shopping_cart(request):
    return render(request, 'store/shopping-cart.html')


def checkout(request):
    return render(request, 'store/checkout.html')


def update_item(request):
    return JsonResponse('Ürün eklendi.', safe=False)


def order_delete(request, id):
    return redirect('mainboard:mainbord')


def order_detail(request, id):
    return render(request, 'store/detail.html')


def order_assign(request, id):
    return render(request, 'store/assign.html')


def order_assign_to_service(request, id, sid):
    return HttpResponseRedirect(Order.get_absolute_url())


def order_service(request, id):
    return HttpResponseRedirect(Order.get_absolute_url())


def order_delivery(request, id):
    return HttpResponseRedirect(Order.get_absolute_url())
