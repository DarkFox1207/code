from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, permissions
from .models import Article
from .serializers import ArticleSerializer
from .forms import ArticleForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def hello_world(request):
    return render(request, 'hello/hello.html')

def article_list(request):
    articles = Article.objects.all().order_by('-pub_date')  # Получаем все статьи, сортируем по дате
    return render(request, 'hello/article_list.html', {'articles': articles})

@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():  # Вызывает clean_title и другие методы валидации
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'hello/article_form.html', {'form': form})

@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():  # Вызывает clean_title и другие методы валидации
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'hello/article_form.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} успешно создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-pub_date')  # Запрос для получения всех статей
    serializer_class = ArticleSerializer  # Сериализатор для статей
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Чтение для всех, остальное для авторизованных