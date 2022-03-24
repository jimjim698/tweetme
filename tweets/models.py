from django.db import models
# Connect Users to Tweet
from django.conf import settings 
import random


# Connect User to Tweet
User = settings.AUTH_USER_MODEL


class TweetLike(models.Model):

    user = models.ForeignKey(User, on_delete= models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

# Create your models here.

class Tweet(models.Model):
    # Maps to SQL data
    # id = models.Autofield(primary_key=True)
    #User
    # CASCADE makes sure all tweets are deleted if the User is deleted.
    # You can also have the tweets user foreign key point to null if you want to save the tweets, <--There's 3 args
    # Create superuser

    parent= models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # User can have many tweets



    content = models.TextField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through= TweetLike)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    # This is how you could change the toString of the model's objects
    # def __str__(self):
    #     return self.content

    #Reverse the ordering
    class Meta:
        ordering = ['-id']

    @property
    def is_retweet(self):
        return self.parent != None

    #Serialize DMO
    # def serialize(self):
    #     return{
    #         "id": self.id,
    #         "content": self.content,
    #         "likes": random.randint(0,200)
    #     }