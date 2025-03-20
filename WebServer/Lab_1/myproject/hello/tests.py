from django.test import TestCase
from .models import Article
from django.utils import timezone
from .forms import ArticleForm
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

#Тест на создание модели
class ArticleModelTest(TestCase):
    def test_article_creation(self):
        # Создаём статью
        article = Article.objects.create(
            title="Тестовая статья",
            content="Это тестовое содержимое статьи."
        )

        # Проверяем, что статья создана корректно
        self.assertEqual(article.title, "Тестовая статья")
        self.assertEqual(article.content, "Это тестовое содержимое статьи.")
        self.assertLessEqual(article.pub_date, timezone.now())  # Дата публикации должна быть не позже текущей

#Проверка правильности форм
class ArticleFormTest(TestCase):
    def test_valid_form(self):
        # Создаём данные для формы
        form_data = {
            'title': 'Тестовая статья',
            'content': 'Это тестовое содержимое статьи.'
        }
        form = ArticleForm(data=form_data)

        # Проверяем, что форма валидна
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Создаём невалидные данные для формы (без заголовка)
        form_data = {
            'title': '',  # Пустой заголовок
            'content': 'Это тестовое содержимое статьи.'
        }
        form = ArticleForm(data=form_data)

        # Проверяем, что форма невалидна
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)  # Проверяем, что есть ошибка в поле "title"

#Проверка работы API
class ArticleAPITest(APITestCase):

    def setUp(self):
        # Создаём тестового пользователя и токен
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Удаляем существующий токен, если он есть
        Token.objects.filter(user=self.user).delete()

        # Создаём новый токен
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')  # Добавляем токен в заголовки

        # Создаём тестовую статью
        self.article = Article.objects.create(
            title="Тестовая статья",
            content="Это тестовое содержимое статьи."
        )
        self.url_list = reverse('article-list')  # URL для списка статей
        self.url_detail = reverse('article-detail', args=[self.article.id])  # URL для конкретной статьи

    def test_get_article_list(self):
        # GET-запрос для получения списка статей
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Проверяем, что вернулась одна статья

    def test_create_article(self):
        # POST-запрос для создания статьи
        data = {
            'title': 'Новая статья',
            'content': 'Текст новой статьи.'
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 2)  # Проверяем, что статья создана

    def test_update_article(self):
        # PUT-запрос для обновления статьи
        data = {
            'title': 'Обновлённый заголовок',
            'content': 'Обновлённый текст.'
        }
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Обновлённый заголовок')  # Проверяем обновление

    def test_delete_article(self):
        # DELETE-запрос для удаления статьи
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 0)  # Проверяем, что статья удалена

#Обработчик ошибок
class ErrorHandlingTest(TestCase):
    def test_404_error(self):
        # Пытаемся получить несуществующую страницу
        response = self.client.get('/несуществующая/страница/')
        self.assertEqual(response.status_code, 404)  # Проверяем, что возвращается 404

    def test_api_404_error(self):
        # Пытаемся получить несуществующую статью через API
        response = self.client.get(reverse('article-detail', args=[999]))  # Несуществующий ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
