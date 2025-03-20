from django.core.cache import caches
from django.shortcuts import render
from django.views.decorators.cache import cache_page 
import time 

@cache_page(60 * 5)  # Кэшировать на 5 минут 
def cached_view(request): 
    time.sleep(5)  # Имитация долгой операции 
    return render(request, 'myapp/cached_view.html', {'time': time.time()})

def low_level_cache_view(request):
    cache_key = 'my_cache_key'
    custom_cache = caches['custom_cache']  # Используем кэш с именем 'custom_cache'
    cached_data = custom_cache.get(cache_key)

    if not cached_data:
        time.sleep(5)  # Имитация долгой операции
        cached_data = time.time()
        custom_cache.set(cache_key, cached_data, 60 * 5)  # Кэшировать на 5 минут
        print("Data cached:", cached_data)  # Отладочное сообщение
    else:
        print("Data retrieved from cache:", cached_data)  # Отладочное сообщение

    return render(request, 'myapp/low_level_cache.html', {'data': cached_data})