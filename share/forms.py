from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from cts.share.models import UserProfile, Comment
from django import forms
import hashlib

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username =forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    def clean(self):
        email = self.cleaned_data.get('email')
        try:
            u = User.objects.get(email=email)
        except User.DoesNotExist:
            return self.cleaned_data

        self._errors['email'] = [u'Email is already in use']
        return self.cleaned_data

class ChangePassForm(forms.Form):
    old_pass = forms.CharField(widget=forms.PasswordInput)
    new_pass1 = forms.CharField(widget=forms.PasswordInput)
    new_pass2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        super(forms.Form, self).clean()
        pass1 = self.cleaned_data.get('new_pass1')
        pass2 = self.cleaned_data.get('new_pass2')
        if pass1 != pass2:
            self._errors['new_pass1'] = [u'Passwords do not match.']
        return self.cleaned_data


class SearchForm(forms.Form):
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    def clean(self):
        username = self.cleaned_data.get('username')
        #If name field is set, verify it is correct if not return error messages
        if username == False:
            self._errors['username'] = [u'Use first name and last name']
        return self.cleaned_data

class SettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('url', 'screen_name', 'description', 'name' , 'location')

    def clean(self):
        super(forms.ModelForm, self).clean()
        if ' ' in self.cleaned_data.get('url'):
            self._errors['url'] = [u'URL cannot contain spaces.']
        return self.cleaned_data

        
class SettingsFormForTwitter(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('screen_name', 'description',  'location', 'thumbnail_url','url')

    def clean(self):
        super(forms.ModelForm, self).clean()
        if False in self.cleaned_data.get('url'):
            self._errors['url'] = [u'URL cannot contain spaces.']
        return self.cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('post', 'public')
        widgets = {
            'post': forms.Textarea(attrs={'cols': 80, 'rows': 7}),
        }


