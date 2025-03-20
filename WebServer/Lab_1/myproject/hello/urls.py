from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, article_list, article_create, article_edit
from . import views
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)  # Регистрация ViewSet для статей

urlpatterns = [
    path('', include(router.urls)),  # Подключаем маршруты DRF
    path('list/', article_list, name='article_list'),
    path('create/', article_create, name='article_create'),
    path('edit/<int:pk>/', article_edit, name='article_edit'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/create/', views.article_create, name='article_create'),
    path('articles/edit/<int:pk>/', views.article_edit, name='article_edit'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('api/', include(router.urls)),  # Подключение маршрутов API
]