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

    total_orders = orders.filter(transaction_id__isnull=False).count()
    delivered = orders.filter(status='Teslim edildi').count()
    transporting = orders.filter(status='Taşımada').count()

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
    delivered = orders.filter(status='Teslim edildi').count()
    transporting = orders.filter(status='Taşımada').count()

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
    # Pie chart
    all_orders = {}
    for order in Order.objects.all():
        for item in order.orderitem_set.all():
            if item.product.name in all_orders:
                all_orders[item.product.name] += 1
            else:
                all_orders[item.product.name] = 1

    labels_pie = list(all_orders.keys())
    data_pie = list(all_orders.values())

    # Bar Chart
    all_service = {}
    for service in Service.objects.all():
        for order in service.order_set.all():
            if order.service.user.username in all_service:
                all_service[order.service.user.username] += 1
            else:
                all_service[order.service.user.username] = 1

    labels_bar = list(all_service.keys())
    data_bar = list(all_service.values())

    # Line Chart
    k = []
    for order in Order.objects.all().order_by('date_ordered__month'):
        m = {}
        m.update({order.date_ordered.strftime('%m'): order.get_cart_total})
        k.append(m)
        del m

    # [{'11': 4.0}, {'11': 5.0}, {'11': 75.0}, {'12': 5.0}, {'12': 54.0}, {'12': 420.0}, {'12': 105.0}, {'12': 5.0},
    #  {'12': 13.0}, {'12': 20.0}]

    result = dict(functools.reduce(operator.add, map(collections.Counter, k)))
    # {'11': 84.0, '12': 622.0}

    labels_line = list(result.keys())
    data_line = list(result.values())

    context = {
        'labels_pie': labels_pie,
        'data_pie': data_pie,
        'labels_bar': labels_bar,
        'data_bar': data_bar,
        'labels_line': labels_line,
        'data_line': data_line
    }
    return render(request, 'mainboard/charts.html', context=context)
