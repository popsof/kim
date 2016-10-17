from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class YoutubeUserManager(UserManager):
	pass

class YoutubeUser(AbstractUser):
	nickname = models.CharField(max_length=24)

	class Meta:
		verbose_name = '사용자'
		verbose_name_plural = '사용자 목록'
	
	def __str__(self):
		return self.username

