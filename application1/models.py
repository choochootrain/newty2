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
