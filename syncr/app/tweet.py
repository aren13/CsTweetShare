import time
from datetime import datetime
#from aren.syncr.app import twitter
import twitter
from django.utils.encoding import smart_unicode
from django.contrib.auth.models import User
from cts.share import comments
from cts.share import forms as myforms
from cts.share.models import UserProfile, Comment # tweet->comment TwitterUser -> UserProfile
#syncr.twitter.models import UserProfile, Tweet

class TwitterSyncr:
    """TwitterSyncr objects sync Twitter information to the Django
    backend. This includes meta data for Twitter users in addition to
    Twitter status updates (Tweets).

    NOTE: Limitations of the Twitter API currently restricts API
    access to only the most recent data in the Twitter system. This
    is for performance reasons (per API docs).

    This app depends on python-twitter:
    http://code.google.com/p/python-twitter/
    
    def __init__(self, username, password):
    	Construct a new TwitterSyncr object.

        Required arguments
          username: the Twitter user to use for authentication
          password: the Twitter user's password to use for auth
    
        self.username = username
        self.api = twitter.Api(username=username, password=password)

        self.user_cache = dict()
    """
    def __init__(self, username, key, secret, token_key, token_secret):  
      
        self.username = username  
        self.api = twitter.Api(  
                             consumer_key=key,   
                             consumer_secret=secret,   
                             access_token_key=token_key,  
                             access_token_secret=token_secret)  
        self.user_cache = dict()  

    def _getUser(self, user):
        """Retrieve Twitter user information, caching for performance
        purposes.
        
        Required arguments
          user: a Twitter username as a string.
        """
        if self.user_cache.has_key(user):
            return self.user_cache[user]
        else:
            tw_user = self.api.GetUser(user)
            self.user_cache[user] = tw_user
            return self.user_cache[user]

    def _syncTwitterUser(self, user):
        """Synchronize a twitter.User object with the Django backend

        Required arguments
          user: a twitter.User object.
                       'description': user.description,
                        'location': user.location,
                        'name': user.name,
                        'thumbnail_url': user.profile_image_url,
  
        """
        default_dict = {'screen_name': user.screen_name,
                        'description': user.description,
                        'location': user.location,
                        'thumbnail_url': user.profile_image_url,
                        'url': user.url,
                        'name': user.name,
                        }
        obj = User.objects.get(username__exact = user.screen_name)
        UserProfile.objects.all().filter(user=obj).update(screen_name= user.screen_name)
        UserProfile.objects.all().filter(user=obj).update(location= user.location)
        UserProfile.objects.all().filter(user=obj).update(description= user.description)
        UserProfile.objects.all().filter(user=obj).update(thumbnail_url= user.profile_image_url)
        UserProfile.objects.all().filter(user=obj).update(url= user.screen_name)
        UserProfile.objects.all().filter(user=obj).update(name= user.name)
## Add all require field with this uptadae and use this func while registration only. 
        return obj

    
    def syncUser(self, user):
        """Synchronize a Twitter user with the Django backend

        Required arguments
          user: a Twitter username as a string
        """
        user_obj = self._syncTwitterUser(self._getUser(user))
        return user_obj

    def _syncTwitterStatus(self, status ):
        """
        Take a twitter.Status object and synchronize it to Django.

        Args:
          status: a twitter.Status object.

        Returns:
          A syncr.twitter.models.Tweet Django object.
        """

        user = self._syncTwitterUser(status.user)
        obj1 = User.objects.get(username__exact = user)
        twitterId=status.id
        UserProfile.objects.all().filter(user=obj1).update(last_tweet= twitterId)
        pub_time = time.strptime(status.created_at, "%a %b %d %H:%M:%S +0000 %Y")
        pub_time = datetime.fromtimestamp(time.mktime(pub_time))
        default_dict = {'sent': pub_time,
                        'twitter_id': status.id,
                        'post': smart_unicode(status.text),
                        'author': user,
                        }
        obj, created = Comment.objects.get_or_create(twitter_id = status.id,
                                                   defaults = default_dict)

        print status.id 
        return obj

    def syncTweet(self, status_id):
        """Synchronize a Twitter status update by id

        Required arguments
          status_id: a Twitter status update id
        """
        status_obj = self.api.GetStatus(status_id)
        return self._syncTwitterStatus(status_obj)

    def syncTwitterUserTweets(self, user):
        """Synchronize a Twitter user's tweets with Django (currently
        only the last 20 updates)

        Required arguments
          user: the Twitter user as string
		count=175
        statuses[-1].GetId()

        edit=UserProfile.objects.all().filter(user=obj)
        edit.update(last_tweet= 123123)
        """
        obj = User.objects.get(username__exact = user)
        statuses = self.api.GetUserTimeline(user,count=50,since_id=obj.get_profile().last_tweet)
        for status in statuses:
            self._syncTwitterStatus(status)


    def syncTwitterUserTweetsRegister(self, user):
        """Synchronize a Twitter user's tweets with Django (currently
        only the last 20 updates)

        Required arguments
          user: the Twitter user as string
		count=175
        since_id='72045145087934464'
        """
        count= 100
        statuses = self.api.GetUserTimeline(user,count=175)

        for status in statuses:
            self._syncTwitterStatus(status)
#######################################################################################
    def syncFriends(self, user):
        """Synchronize a Twitter user's friends with Django.

        Required arguments
          user: the Twitter username as a string
        """
        user_obj = self._syncTwitterUser(self._getUser(user))
        friends = self.api.GetFriends(user)

        # sync our list of twitter.User objs as into ORM
        for friend in friends:
            obj = self._syncTwitterUser(friend)
            user_obj.friends.add(obj)

    def syncFollowers(self):
        """Synchronize the Twitter user's followers with Django. This
        only works for the username who is authenticated in the API
        object.
        """
        user_obj = self._syncTwitterUser(self._getUser(self.username))
        followers = self.api.GetFollowers()

        # sync our list of twitter.User objs into ORM
        for follower in followers:
            obj = self._syncTwitterUser(follower)
            user_obj.followers.add(obj)

    def syncFriendsTweets(self, user):
        """Synchronize the tweets of a Twitter user's friends (currently
        only the last 20 updates). Also automatically add these users
        as friends in the Django database, if they aren't already.

        Required arguments
          user: the Twitter username whose friend's tweets will sync
        """
        friend_updates = self.api.GetFriendsTimeline(user)
        user_obj = self._syncTwitterUser(self._getUser(user))
        
        # loop through twitter.Status objects and sync them
        for update in friend_updates:
            self._syncTwitterStatus(update)
            friend = self._syncTwitterUser(update.user)
            user_obj.friends.add(friend)

