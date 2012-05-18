from django.conf.urls.defaults import *

urlpatterns = patterns( 'share.views',
    (r'^$', 'index' , {} , 'index'),
    (r'^tweetboard/$', 'tweetboard', {} ,'tweetboard'),
    (r'^settings/$', 'settings', {}, 'settings'),
    (r'^settings/friends/$', 'manage_friends', {},'manage_friends'),
    (r'^settings/friends/(?P<id>\d+)/$', 'manage_friend', {} ,'manage_friend'),
    (r'^settings/password/$', 'change_pass', {} ,'change_pass'),
    (r'^users/(?P<url>\w+)/$', 'profile', {} ,'profile'),
    (r'^users/(?P<url>\w+)/friends/$', 'view_friends', {}, 'view_friends'),
    (r'^invite/(?P<url>\w+)/$', 'invite',{} , 'invite'),
    (r'^invite/accept/(?P<url>\w+)/$', 'accept_inv', {} ,'accept_inv'),
    (r'^invite/ignore/(?P<url>\w+)/$', 'ignore_inv', {},'ignore_inv'),
    (r'^search/$', 'search', {} ,'search'),
    (r'^about/$', 'about', {} ,'about'),
)

urlpatterns += patterns('share.auth',	
	(r'^login/', 'login', {} , 'login' ),
	(r'^logout/', 'logout',{} ,'logout' ),
	(r'^accounts/login', 'login',{} ,'login'),
	(r'^register/', 'register', {},'register'),
)

urlpatterns +=patterns('share.comments', 
    (r'^users/(?P<url>\w+)/comment/$', 'post',{} ,'post' ),
    (r'^users/(?P<url>\w+)/comment/(?P<comment_id>\d+)/delete/$', 'delete',{} , 'delete'),
    (r'^users/(?P<url>\w+)/comment/(?P<comment_id>\d+)/reply/$', 'reply',{} , 'reply'),
)



