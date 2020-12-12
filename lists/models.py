from django.db import models
from django.urls import reverse


class List(models.Model):
    def get_absolute_url(self):
        return reverse('view-list', args=[self.id])


class Item(models.Model):
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
    text = models.TextField(default='')

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ('list', 'text')
