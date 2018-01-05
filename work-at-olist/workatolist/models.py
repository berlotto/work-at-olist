from django.db import models


class Channel(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='childs_set', null=True)

    def __str__(self):
        return self.name
