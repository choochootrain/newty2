from django.db import models
from django.contrib.auth.models import User

class UserExtended(models.Model):
    userOther = models.ForeignKey(User, unique = True)
    username = models.CharField(max_length = 40)
    location = models.CharField(max_length = 50)
    uuid = models.CharField(max_length = 32)
    numHelped = models.IntegerField()
    weight = models.IntegerField()
    confirmed = models.BooleanField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    def __unicode__(self):
        return self.username

"""
    requester= models.ForeignKey(UserExtended, related_name="requester")
    fulfiller = models.ForeignKey(UserExtended, related_name="fulfiller")
    large_text = models.TextField()
    date = models.DateTimeField()
    boolean = modles.BooleanField()
    null_and_blank = models.IntegerField(blank=True, null=True)
"""

class NewsSource(models.Model):
    name = models.CharField(max_length = 300)
    updated = models.DateTimeField(blank=True, null=True)


class Article(models.Model):
    title = models.CharField(max_length = 300)
    body = models.CharField(max_length = 100000)
    date = models.DateTimeField()
    url = models.CharField(max_length = 300)
    file_path = models.CharField(max_length = 300)
    news_source = models.ForeignKey(NewsSource)
    

class BodyIndex(models.Model):
    article = models.ForeignKey(Article)
    word_count = models.IntegerField()
    total_word_count = models.IntegerField()
    percentage = models.FloatField()
    word = models.CharField(max_length = 50)
    #date = models.DateTimeField()
    

class TitleIndex(models.Model):
    article = models.ForeignKey(Article)
    word_count = models.IntegerField()
    total_word_count = models.IntegerField()
    percentage = models.FloatField()
    word = models.CharField(max_length = 50)
    #date = models.DateTimeField()

class ErrorsParsing(models.Model):
    file_path = models.CharField(max_length = 300)
