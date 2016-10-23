from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    kind = models.CharField(max_length=100)
    key = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    desc = models.TextField(blank=True)
    published_date = models.DateTimeField()
    thumbnail = models.URLField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

