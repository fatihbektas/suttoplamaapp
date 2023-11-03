from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from account.forms import CreateUserForm
from django.contrib import messages


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # username ve password ile authenticate ol
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mainboard:mainboard')
        else:
            messages.info(
                request, 'Kullanıcı adı ve/veya şifre geçerli değil!')

    context = {}

    return render(request, 'account/login.html', context=context)


def register(request):
    form = CreateUserForm
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid:
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, username +
                             'kullanıcısı için hesap oluşturuldu.')
            return redirect('account:login')
    context = {'form': form}
    return render(request, 'account/register.html', context=context)


def logout(request):
    orders = request.user.customer.order_set.all()
    for order in orders:
        if order.transaction_id is None:
            order.delete()
    logout(request)
    return redirect('account:login')
