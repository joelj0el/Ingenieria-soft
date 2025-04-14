# usuarios/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views import View
from .forms import FormularioRegistro, FormularioLogin

class RegistroView(View):
    def get(self, request):
        form = FormularioRegistro()
        return render(request, 'usuarios/registro.html', {'form': form})
    
    def post(self, request):
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        return render(request, 'usuarios/registro.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = FormularioLogin()
        return render(request, 'usuarios/login.html', {'form': form})
    
    def post(self, request):
        form = FormularioLogin(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, 'usuarios/login.html', {'form': form})