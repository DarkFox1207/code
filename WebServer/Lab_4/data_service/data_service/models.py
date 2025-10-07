from django.db import models

class SecureData(models.Model):
    owner_id = models.IntegerField()  # Связь с пользователем в Auth Service
    content = models.TextField()
    encrypted_content = models.BinaryField()  # Шифрование данных
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Защищенные данные'
        verbose_name_plural = 'Защищенные данные'