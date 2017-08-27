from django.db import models
from django.contrib.auth.models import User

class Muppet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    can_post = models.BooleanField(default=True)
    
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(Muppet)
    pub_date = models.DateField()
    headline = models.CharField(max_length=200)
    content = models.TextField()

