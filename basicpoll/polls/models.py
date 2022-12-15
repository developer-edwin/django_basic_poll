from django.db import models

class Question(models.Model):
    # id <- automatic
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("publication date")

class Choices(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)