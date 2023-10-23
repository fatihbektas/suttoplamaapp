from django.shortcuts import redirect, render

def login(request):
    return render(request, 'account/login.html')

def register(request):
    return render(request, 'account/register.html')

def logout(request):
    return redirect('account:login')
