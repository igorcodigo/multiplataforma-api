"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.http import HttpResponse
import time

def hello_world(request):
    return HttpResponse("Hello World!")

def teste_carga(request):
    # Find prime numbers up to limit as a load test
    limit = 500000
    primes = []
    
    start_time = time.time()
    for num in range(2, limit + 1):
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    
    execution_time = time.time() - start_time
    
    return HttpResponse(
        f"Teste de carga concluído.<br>"
        f"Encontrados {len(primes)} números primos até {limit}.<br>"
        f"Tempo de execução: {execution_time:.4f} segundos."
    )

#loaderio eh um site de teste de carga
def loaderio_verification(request):
    return HttpResponse("loaderio-550a90297d4965f85469a81bb57209b6", content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contas/', include('accounts.urls')),
    path('hello/', hello_world, name='hello_world'),
    path('teste-carga/', teste_carga, name='teste_carga'),
    path('loaderio-550a90297d4965f85469a81bb57209b6.txt', loaderio_verification, name='loaderio_verification'),
    path('loaderio-550a90297d4965f85469a81bb57209b6.html', loaderio_verification, name='loaderio_verification_html'),
    path('loaderio-550a90297d4965f85469a81bb57209b6/', loaderio_verification, name='loaderio_verification_path'),
]

home_url = '/admin'
def custom_404_view(request, exception):
    if request.user.is_authenticated:
        return redirect(home_url)
    else:
        return redirect('login')

# Definir o handler404
handler404 = custom_404_view