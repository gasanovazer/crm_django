from django.contrib.auth.models import User
from django.db import models

from team.models import Team


# Create your models here.
class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name="userprofile", on_delete=models.CASCADE)
    active_team = models.ForeignKey(Team, related_name='userprofile', blank=True, null=True, on_delete=models.CASCADE)
    
    # def __str__(self) -> str:
    #     return self.name