# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import uuid

# Create your models here.



class UserModel(models.Model):  #model for storing details of user in database
    name=models.CharField(max_length=100)
    email=models.EmailField()
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)




class Sessiontoken(models.Model):   #model for session token
    user=models.ForeignKey(UserModel)
    session_token=models.CharField(max_length=255)
    created_on=models.DateTimeField(auto_now_add=True)
    is_valid=models.BooleanField(default=True)

    def create_token(self):
        self.session_token=uuid.uuid4()





class PostModel(models.Model):  #model for posting
  user = models.ForeignKey(UserModel)
  image = models.FileField(upload_to='user_images')
  image_url = models.CharField(max_length=255)
  caption = models.CharField(max_length=240)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  has_liked=False




  @property
  def like_count(self): #for likes on comment
    return len(LikeModel.objects.filter(post=self))



  @property
  def comments(self):
    return CommentModel.objects.filter(post=self).order_by('-created_on')




class LikeModel(models.Model):  #model for like
	user = models.ForeignKey(UserModel)
	post = models.ForeignKey(PostModel)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)






class CommentModel(models.Model):   #for comment structure
    user = models.ForeignKey(UserModel)
    post = models.ForeignKey(PostModel)
    comment_text = models.CharField(max_length=500)
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)




class CategoryModel(models.Model):
    post = models.ForeignKey(PostModel)
    category_text = models.CharField(max_length=555)



