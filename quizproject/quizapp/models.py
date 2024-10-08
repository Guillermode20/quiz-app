from django.db import models

# Create your models here.

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_text = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=200)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.question_text
    
class Score(models.Model):
    score = models.IntegerField(default=0)
    
    def __str__(self):
        return {self.score}