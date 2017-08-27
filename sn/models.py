from django.db import models
from django.contrib.auth.models import User

class Muppet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    can_post = models.BooleanField(default=True)
    
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User)
    pub_date = models.DateTimeField()
    headline = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.headline
