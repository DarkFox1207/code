from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')  # Поля, отображаемые в списке статей
    search_fields = ('title', 'content')  # Поля, по которым можно искать
    list_filter = ('pub_date',)  # Фильтры по дате