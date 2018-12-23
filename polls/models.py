from django.db import models

class Question(models.Model):
	ques = models.CharField(max_length = 100)
	pub_date = models.DateTimeField('publishing date')
	def __str__(self):
		return self.ques

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete = models.CASCADE, related_name = 'choices') #maintaining a backward relationship with referred model
	choice_text = models.CharField(max_length = 10)
	votes = models.IntegerField(default = 0)
	def __str__(self):
		return self.choice_text

