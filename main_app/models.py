from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.

class Fav_Team(models.Model):
    team_id = models.CharField(max_length=100)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Fav_Player(models.Model):
    player_id = models.CharField(max_length=100)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

class Fav_List(models.Model):
    name = models.CharField(max_length=100)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    fav_players = models.ManyToManyField(Fav_Player)
