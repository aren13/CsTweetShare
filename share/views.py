from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from share.forms import *
from share import util
from share.models import UserProfile,  Invite, Comment
from syncr.app.tweet import *
import datetime

def r2r(request, v,c, mimetype="text/html"):
	return render_to_response(v,c, context_instance=RequestContext(request), mimetype=mimetype)

def about(request):
	return r2r(request, 'about.html', {})

@login_required
def index(request):
	return HttpResponseRedirect('/tweetboard/')

@login_required
def tweetboard(request):
	last_week = datetime.datetime.now() - datetime.timedelta(days=7)
	user_profile = request.user.get_profile()
	updates = []
	form = CommentForm()
    # Add user's status updates and comments from friends to user
	my_comments = user_profile.comments.filter(sent__gte=last_week)
	up = []
	for c in my_comments:
		up.append(c)
    # Add user's friends' status updates
	friends = list(user_profile.friends.all())
    #reset up in case friends is empty
	for f in friends:
		comments = f.get_profile().comments.filter(sent__gte=last_week)
		for c in comments:
			up.append(c)
	up.sort(key=lambda x: x.sent, reverse=True)
	return r2r(request, 'tweetboard.html', {'updates': updates, 'form': form})

@login_required
def settings(request):
	user = request.user.get_profile()
	form = SettingsForm(request.POST or None, instance=user)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect('/tweetboard/')
	return r2r(request, 'settings/settings.html', {'form': form})
			
@login_required
def manage_friends(request):
	return r2r(request, 'settings/friends.html', {})

@login_required
def manage_friend(request, id):
	other_user = get_object_or_404(User, pk=id)
	return r2r(request, 'settings/friend.html', {'friend': other_user})

@login_required
def change_pass(request):
	form = ChangePassForm(request.POST or None)
	user = request.user
	if form.is_valid():
		if not auth.models.check_password(form.cleaned_data['old_pass'], user.password):
			form._errors['old_pass'] = [u'Old password is incorrect']
		else:
			user.set_password(form.cleaned_data['new_pass1'])
			user.save()
			return HttpResponseRedirect('/tweetboard/')
	return r2r(request, 'settings/change_pass.html', {'form': form})

@login_required
def profile(request, url):
	user = request.user
	other_user = get_object_or_404(UserProfile, url=url).user
	t = TwitterSyncr('aren_13','uzXnuF1K7Xwn1Fu4A43EaQ','gwog9Z2jgxBlR7VxQ0xBqhZglalokHHTTdTWc3rE','eK9WPBFunh7CRP2kSazjSJ452siayIfwtWzJebmITw','UhUaenJCVT326lDHHUNM2B8XIhvJv1h1rHW5KJjU',)  
	t.syncUser(request.user.username)
	t.syncTwitterUserTweets(request.user.username) # FIXME: sync with time interval
	t.syncTwitterUserTweets(other_user.username) # FIXME: sync with time interval
	commentss = list(Comment.objects.all())  
	try:
		inv = other_user.get_profile().invites.get(sender=user)
		invited = True
	except Invite.DoesNotExist:
		invited = False
    # post a comment
	if util.can_users_interract(user, other_user) or user.get_profile().url == url:
		form = CommentForm()
		return r2r(request, 'profile/profile.html', {'other_user': other_user, 'commentss': commentss ,'form': form, 'invited': invited })
	return r2r(request, 'profile/profile.html', {'other_user': other_user, 'commentss': commentss , 'invited': invited })

@login_required
def view_friends(request, url):
	other_user = get_object_or_404(UserProfile, url=url).user
	return r2r(request, 'profile/friends.html', {'other_user': other_user})

@login_required
def invite(request, url):
	sender = request.user
	prof = get_object_or_404(UserProfile, url=url)
    #check for existing invites
	try:
		inv = prof.invites.get(sender=sender)
	except Invite.DoesNotExist:
		inv = Invite.objects.create(
                sender=sender,
                user=prof.user,
                sent=datetime.datetime.now(),
                )
		prof.invites.add(inv)
	return HttpResponseRedirect('/users/'+prof.url+'/')

@login_required
def accept_inv(request, url):
	user = request.user
	sender = UserProfile.objects.get(url=url).user
	inv = Invite.objects.get(user=user, sender=sender)
	user.get_profile().friends.add(sender)
	sender.get_profile().friends.add(user)
	inv.delete()
	return HttpResponseRedirect('/tweetboard/')

@login_required
def ignore_inv(request, url):
	sender = User.objects.get(url=url).sender
	inv = Invite.objects.get(user=request.user, sender=sender)
	inv.delete()
	return HttpResponseRedirect('/tweetboard/')

@login_required
def search(request):
	form = SearchForm()
	results = None
	form = SearchForm(request.POST or None)
	if form.is_valid():
		email = form.cleaned_data['email']
		username = form.cleaned_data['username']
		if email:
			results = User.objects.filter(email=email)
		elif username:
			results = User.objects.filter(username__iexact=username)
	return r2r(request, 'search.html', {'form': form, 'results': results})


