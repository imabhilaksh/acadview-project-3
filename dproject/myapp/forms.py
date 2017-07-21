from django import forms

from myapp.models import UserModel,PostModel,CommentModel,LikeModel



class Signupform(forms.ModelForm): #form for signing up
    class Meta:
        model=UserModel
        fields=['email','name','password','username']



class Loginform(forms.ModelForm):   #form for logging in
    class Meta:
        model=UserModel
        fields=['username','password']


class Postform(forms.ModelForm):    #form for posting images
    class Meta:
        model=PostModel
        fields=['image','caption']


class LikeForm(forms.ModelForm):    #form for like

    class Meta:
        model = LikeModel
        fields=['post']


class CommentForm(forms.ModelForm):  #form for comments

    class Meta:
        model = CommentModel
        fields = ['comment_text', 'post']




