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
        parent_path = ""
        obj = self
        while obj.parent is not None:
            parent_path = obj.parent.name + "/" + parent_path
            obj = obj.parent
        return parent_path + self.name
