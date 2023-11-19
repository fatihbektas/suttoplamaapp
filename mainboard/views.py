from django.shortcuts import render
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from suttoplamaapp.decorators import *
from account.forms import *
from store.models import *
import functools
import operator
import collections


@login_required(login_url='account:login')
@allowed_users(allowed_roles=['admin'])
def mainboard(request):
    orders = Order.objects.all()
    customers = Customer.objects.all().exclude(user__groups__name='service')

    total_orders = orders.filter(transaction_id__isnull=False).count()
    delivered = orders.filter(status='Teslim edildi').count()
    transporting = orders.filter(status='Taşımada').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'transporting': transporting,
    }

    return render(request, 'mainboard/mainboard.html', context=context)


@login_required(login_url='account:login')
@allowed_users(allowed_roles=['customer'])
def user_page(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    transporting = orders.filter(status='Transporting').count()

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'transporting': transporting,
    }

    return render(request, 'mainboard/user.html', context=context)


@login_required(login_url='account:login')
@allowed_users(allowed_roles=['service'])
def service_page(request):
    orders = request.user.service.order_set.all()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    transporting = orders.filter(status='Transporting').count()

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'transporting': transporting,
    }

    return render(request, 'mainboard/service.html', context=context)


@login_required(login_url='account:login')
def account_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form': form}

    return render(request, 'mainboard/account-settings.html', context=context)


@login_required(login_url='account:login')
@allowed_users(allowed_roles=['admin'])
def view_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
    }
    return render(request, 'mainboard/customer.html', context=context)


@login_required(login_url='account:login')
@allowed_users(allowed_roles=['admin'])
def view_chart(request):
    # TODO: Chart view ayarlanacak
    return render(request, 'mainboard/charts.html')
