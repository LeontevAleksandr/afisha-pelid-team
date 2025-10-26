from django.db import models
from ckeditor.fields import RichTextField


class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description_short = models.TextField(blank=True, verbose_name="Короткое описание")
    description_long = RichTextField(blank=True, verbose_name="Полное описание")
    lng = models.FloatField(verbose_name="Долгота")
    lat = models.FloatField(verbose_name="Широта")

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images', verbose_name="Место")
    image = models.ImageField(upload_to='places/', verbose_name="Картинка")
    position = models.PositiveIntegerField(default=0, verbose_name="Позиция")

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"
        ordering = ['position']

    def __str__(self):
        return f"{self.place.title} - {self.position}"