from django.db import models
from django.utils.text import slugify


class Phone(models.Model):

    name = models.TextField()
    slug = models.SlugField(blank=True)
    price = models.IntegerField()
    image = models.URLField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()

    def save(self, *args, **kwargs):
        """
        Расширяет метод save.
        Если поле slug не заполнено, то заполняет его использую поле name
        при сохранении модели.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super(Phone, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
