from django.db import models
from django.contrib.auth.models import User

class Quest(models.Model):
    quest_text = models.CharField(max_length=500)
    id = models.IntegerField(primary_key=True)

class Choice(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    votes = models.IntegerField()

class UserProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    page = models.IntegerField(default=1)
