from django.http import JsonResponse
from django.shortcuts import render

def store(request):
    return render(request, 'store/store.html')

def card(request):
    return render(request, 'store/card.html')

def checkout(request):
    return render(request, 'store/checkout.html')

def update_item(request):
    return JsonResponse('Ürün eklendi.', safe=False)