from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.

class Fav_Team(models.Model):
    team_id = models.CharField(max_length=100)

    user = models.ForeignKey(User, on_delete=models.CASCADE)



class Fav_List(models.Model):
    name = models.CharField(max_length=100)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('favlist_detail', kwargs={'pk': self.id})


class Fav_Player(models.Model):
    player_id = models.CharField(max_length=100)
    pos = models.CharField(max_length=10)
    team = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    
    fav_list = models.ForeignKey(Fav_List, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.player_id}'