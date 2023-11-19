from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from account.forms import CreateUserForm
from django.contrib import messages


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # username ve password ile authenticate ol
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.groups.all()[0].name == "customer":
                return redirect('mainboard:user-page')
            elif request.user.groups.all()[0].name == "service":
                return redirect('mainboard:service-page')
            else:
                return redirect('mainboard:mainboard')
        else:
            messages.info(
                request, 'Kullanıcı adı ve/veya şifre geçerli değil!')
    context = {}
    return render(request, 'account/login.html', context)


def register_user(request):
    context = {}
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:login')
        else:
            messages.info(request, 'Gerekli alanları doldurun!')
    else:
        form = CreateUserForm()
    context = {'form': form}
    return render(request, 'account/register.html', context=context)


def logout_user(request):
    # orders = request.user.customer.order_set.all()
    # for order in orders:
    #     if order.transaction_id is None:
    #         order.delete()
    logout(request)
    return redirect('account:login')
