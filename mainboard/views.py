from django.shortcuts import render

def mainboard(request):
    return render(request, 'mainboard/mainboard.html')

def user_page(request):
    return render(request, 'mainboard/user.html')

def service_page(request):
    return render(request, 'mainboard/service.html')

def account_settings(request):
    return render(request, 'mainboard/account_settings.html')

def view_customer(request, pk):
    return render(request, 'mainboard/customer.html')

def view_chart(request):
    return render(request, 'mainboard/charts.html')
