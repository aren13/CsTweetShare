from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from cts.share import forms as myforms
from cts.share import util
from cts.share.models import UserProfile, Comment, SubComment
import datetime

@login_required
def post(request, url):
	user = request.user
	other_user = request.user.get_profile().user
	if request.method == 'POST':
		if util.can_users_interract(user, other_user):
			comment = Comment.objects.create(
                    author=user,
                    read=False,
                    sent = datetime.datetime.now(),
					twitter_id = 2 #TODO: autogenerate or get from user.profile
                    )
			form = myforms.CommentForm(request.POST, instance=comment)
			comment = form.save()
			other_user.get_profile().comments.add(comment)
	return HttpResponseRedirect('/users/'+other_user.get_profile().url+'/')

@login_required
def reply(request, url, comment_id):
	user = request.user
	other_user = get_object_or_404(UserProfile, url=url).user
	if request.method == 'POST':
		if util.can_users_interract(user, other_user):
			comment = get_object_or_404(Comment, id=comment_id)
			subcomment = SubComment.objects.create(
                    author=user,
                    post=request.POST['post'],
                    read=False,
                    sent=datetime.datetime.now(),
                    parent=comment,
                    )
			comment.subcomments.add(subcomment)
	return HttpResponseRedirect('/profile/'+other_user.get_profile().url)

@login_required
def delete(request, url, comment_id):
	user_profile = request.user.get_profile()
	comment = Comment.objects.get(id=comment_id)
	if comment in user_profile.comments.all():
		user_profile.comments.remove(comment)
		comment.delete()
	return HttpResponseRedirect('/tweetboard/')

