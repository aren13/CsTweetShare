from django.contrib import admin
from share.models import UserProfile, Comment , SubComment

class CommentAdmin(admin.ModelAdmin):
	date_hierarchy = 'sent'
	list_display = ('post', 'sent', 'read' , 'author', 'twitter_id' )

class SubCommentAdmin(admin.ModelAdmin):
	date_hierarchy = 'sent'
	list_display = ('post', 'sent', 'read' , 'author', 'twitter_id' )
	
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'last_tweet', 'description', 'location', 'name', 'thumbnail_url', 'url' )


admin.site.register(SubComment, SubCommentAdmin)	
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

