from django.db import models

# Create your models here.

NULLABLE = {'null': True, 'blank': True}


class Blog(models.Model):
    """
    Модель для блога
    """
    header = models.CharField(max_length=100, verbose_name='заголовок')
    slug = models.CharField(max_length=150, verbose_name=' человекопонятный URL', **NULLABLE)
    content = models.TextField(verbose_name='содержимое')
    image = models.ImageField(upload_to='blog/', verbose_name='превью (изображение)', **NULLABLE)
    date_of_create = models.DateTimeField(verbose_name='дата создания')

    sign_of_publication = models.BooleanField(default=True, verbose_name='признак публикации', **NULLABLE)
    quantity_of_views = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __int__(self):
        return f'{self.header} '

    def __str__(self):
        return f'{self.header}'

    class Meta:
        verbose_name = 'блоговая запись'
        verbose_name_plural = 'блоговые записи'
        ordering = ('header',)
