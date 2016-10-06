import datetime
from django.db import models
from django.utils import timezone


# Create your models here.
class Question(models.Model):
	question_text = models.CharField('질문 내용', max_length=200)
	pub_date = models.DateTimeField('date published')

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

	def __str__(self):
		return "질문 [{}]".format( self.question_text )

class Choice(models.Model):
	question = models.ForeignKey(Question,on_delete=models.CASCADE )
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return "선택 [{}]".format( self.choice_text )

