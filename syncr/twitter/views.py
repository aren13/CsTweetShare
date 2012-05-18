from django.shortcuts import render_to_response
from django.http import HttpResponse
#from cts.syncr.tweet import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.conf import settings
from cts.syncr.app.tweet import TwitterSyncr
import twitter


""" Change api related fields with your own keys"""
def tweet(request):
	api = twitter.Api(consumer_key='uzXnuF1K7Xwn1Fu4A43EaQ',
                           consumer_secret='gwog9Z2jgxBlR7VxQ0xBqhZglalokHHTTdTWc3rE',
                            access_token_key='eK9WPBFunh7CRP2kSazjSJ452siayIfwtWzJebmITw',
                            access_token_secret='UhUaenJCVT326lDHHUNM2B8XIhvJv1h1rHW5KJjU')

	user = "aren_13" 
	count = 130 
	api.GetUserTimeline(screen_name=user,max_id=62965497699893250)
    
	return HttpResponse("Welcome  arda" )

	

