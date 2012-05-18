from syncr.app.tweet import TwitterSyncr   
import time
from datetime import datetime
import twitter
from django.utils.encoding import smart_unicode
from syncr.twitter.models import TwitterUser, Tweet 

def tweet(request):
	
 


	t = TwitterSyncr ('aren_13','uzXnuF1K7Xwn1Fu4A43EaQ',
'gwog9Z2jgxBlR7VxQ0xBqhZglalokHHTTdTWc3rE',
'eK9WPBFunh7CRP2kSazjSJ452siayIfwtWzJebmITw',
'UhUaenJCVT326lDHHUNM2B8XIhvJv1h1rHW5KJjU',)  
      

      
	t.syncUser('aren_13')  
      
#3. get tweets for the Twitter user (so it will import tweets from Twitter to your DB)  
      
	t.syncTwitterUserTweets('aren_13')  
      
      
      
#4. grab user from database and it's tweets  
      
	user = TwitterUser.objects.get(screen_name="aren_13")  
      
	tweets = Tweet.objects.filter(user=user)  
		    
	return HttpResponse("Welcome  %s" % arda)
