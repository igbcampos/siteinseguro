from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Comentario(models.Model):
    autor= models.ForeignKey(User,on_delete=models.CASCADE)
    titulo= models.CharField(max_length=256, blank=True, null=True)
    texto= models.TextField(blank=False, null=False)
    data= models.DateTimeField(default=timezone.now)