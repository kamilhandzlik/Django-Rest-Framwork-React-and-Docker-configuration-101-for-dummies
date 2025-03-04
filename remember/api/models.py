from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    publish_date = models.DateField(blank=True)

    def __str__(self):
        return f"{self.title or 'Brak tytułu'} - {self.author or 'Brak autora'} - {self.publish_date or 'Brak daty'}"
