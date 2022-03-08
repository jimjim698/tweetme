from django.db import models
import random

# Create your models here.

class Tweet(models.Model):
    # Maps to SQL data
    # id = models.Autofield(primary_key=True)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)


    #Reverse the ordering
    class Meta:
        ordering = ['-id']

    #Serialize DMO
    def serialize(self):
        return{
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0,200)
        }