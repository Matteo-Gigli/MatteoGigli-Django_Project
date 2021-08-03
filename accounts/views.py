from django.shortcuts import render, redirect
from .forms import Registration
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate



def registration(request):
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/homepage/')

    else:
        form = Registration()
        context = {'form': form}
        return render(request, 'registration_form.html', context)


