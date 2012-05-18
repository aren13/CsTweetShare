from django.db import models
from django.contrib.auth.models import User

#Tweets 
class Comment(models.Model):
    class Meta:
        get_latest_by = 'sent'
        ordering = ['-sent']

    author = models.ForeignKey(User) #sender
    post = models.CharField(max_length=500) # text
    read = models.BooleanField() #
    sent = models.DateTimeField() #date
    public = models.BooleanField(default=True)#for posting tweet.(But inside)
    subcomments = models.ManyToManyField('SubComment', null=True, blank=True) #comments for tweets.
    twitter_id  = models.BigIntegerField(null=True) #tweet_id.

    def __unicode__(self):
        return u'%s ' % (self.author)

class SubComment(Comment):
    parent = models.ForeignKey(Comment, related_name='parent')

#Friend invite
class Invite(models.Model):
    user = models.ForeignKey(User)
    sender = models.ForeignKey(User, related_name='sender')
    sent = models.DateTimeField()

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    friends = models.ManyToManyField(User, null=True, blank=True, related_name='friends')
    invites = models.ManyToManyField(Invite, null=True, blank=True, related_name='invites')
    comments = models.ManyToManyField(Comment, null=True, blank=True)
    url = models.CharField(max_length=20, unique=True)
#For Twitter 
    last_tweet=models.BigIntegerField(blank=True, null=True);
    screen_name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True, null=True)
    location    = models.CharField(max_length=50, blank=True, null=True)
    name        = models.CharField(max_length=50, blank=True, null=True)
    thumbnail_url = models.URLField()


    def __unicode__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

#import util
#def create_profile(sender, **kwargs):
#    if kwargs.get('created', False):
#        user = kwargs.get('instance')
#        url = util.gen_url()
#        UserProfile.objects.create(user=user, url=url)

#from django.db.models.signals import post_save
#post_save.connect(create_profile, sender=User)

