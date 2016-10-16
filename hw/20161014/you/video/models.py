from django.db import models

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=32, unique=True)
	created_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name
	
class Video(models.Model):
	category = models.ForeignKey(Category,on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	url = models.URLField()
	view_count = models.IntegerField(default=0)
	like_count = models.IntegerField(default=0)
	created_date = models.DateTimeField(auto_now_add=True)
	key = models.CharField(max_length=32)

	def __str__(self):
		return self.title
