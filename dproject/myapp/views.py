# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages

from django.conf import settings

from django.core.mail import send_mail

from imgurpython import ImgurClient

from django.shortcuts import render,redirect

from myapp.models import UserModel,Sessiontoken,PostModel,LikeModel,CommentModel,CategoryModel

from forms import Signupform,Loginform,Postform,LikeForm,CommentForm

from django.contrib.auth.hashers import make_password,check_password

from dproject.settings import BASE_DIR

from clarifai.rest import ClarifaiApp

# Create your views here.


clarafai_api_key='b2c31f506f4849059f0ba5efa3822036'

def signup_view(request):           #function for performing signup
    if request.method == 'GET':     #only shows the signup form
        form = Signupform()
        return render(request, 'index.html', {'form': form})
    elif request.method=="POST":
        form=Signupform(request.POST)
        if form.is_valid():         #checking if the form is valid or not
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            name=form.cleaned_data['name']
            password=form.cleaned_data['password']
            user=UserModel(name=name,username=username,password=make_password(password),email=email)
            user.save()
            subject='Django App '
            message="Successfully Signed Up"
            from_email=settings.EMAIL_HOST_USER
            to_list=[user.email,settings.EMAIL_HOST_USER]
            send_mail(subject,message,from_email,to_list,fail_silently=True)
            return render(request,'success.html')       #account created





def login_view(request):        #function for performing login
    response_data = {}
    if request.method == "POST":
        form = Loginform(request.POST)      #for submitting the form
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserModel.objects.filter(username=username).first()

            if user:
                if check_password(password, user.password):
                    token = Sessiontoken(user=user)
                    token.create_token()#create a token
                    token.save()#save  token
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response#redirects to the feeds page
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'

    elif request.method == 'GET':
        form = Loginform()

    response_data['form'] = form
    return render(request, 'login.html', response_data)




#for post viewing
def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'POST':
            form = Postform(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()

                path = str(BASE_DIR + post.image.url)
                client = ImgurClient('4669283752027f6','8f2acc853f96e16e10e2c112bfe945b6d8e1dc08')
                post.image_url = client.upload_from_path(path, anon=True)['link']
                post.save()

                return redirect('/feed/')
        else:
            form = Postform()
        return render(request, 'post.html', {'form': form})
    else:
        return redirect('/login/')





#for feed viewing
def feed_view(request):
    user = check_validation(request)
    if user:

        posts = PostModel.objects.all().order_by('created_on')
        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True

        return render(request, 'feed.html', {'posts': posts})


    return redirect('/login/')





# for liking and like viewing
def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():

            post_id = form.cleaned_data.get('post').id
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
                d=LikeModel.objects.filter(post_id=post_id,user=user).first()
                to=d.user.email
                subject = 'Django App '
                message = "Someone just liked your post "
                from_email = settings.EMAIL_HOST_USER
                to_list = [to, settings.EMAIL_HOST_USER]
                send_mail(subject, message, from_email, to_list, fail_silently=True)




            else:
                existing_like.delete()
            return redirect('/feed/')
    else:
        return redirect('/login/')





#for comments and viewing
def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()
            subject = 'Django App '
            message = "Someone just commented on your post"
            from_email = settings.EMAIL_HOST_USER
            to_list = [comment.user.email, settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email, to_list, fail_silently=True)

            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')




# For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = Sessiontoken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
                return session.user
    else:
        return None



def logout_view(request):   #for logging out the user
    request.session.modified = True
    response = redirect('/login/')
    response.delete_cookie(key='session_token')
    return response



def cat_view(request):
    user = check_validation(request)
    if user:

        posts = PostModel.objects.all().order_by('-created_on')

        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True

        return render(request, 'category.html', {'posts': posts})
    else:

        return redirect('/login/')



def add_category(post):
    app = ClarifaiApp(api_key=clarafai_api_key)
    model = app.models.get("general-v1.3")
    response = model.predict_by_url(url=post.image_url)

    if response["status"]["code"] == 10000:
        if response["outputs"]:
            if response["outputs"][0]["data"]:
                if response["outputs"][0]["data"]["concepts"]:
                    for index in range(0, len(response["outputs"][0]["data"]["concepts"])):
                        category = CategoryModel(post=post, category_text = response["outputs"][0]["data"]["concepts"][index]["name"])
                        category.save()
                else:
                    print "No Concepts List Error"
            else:
                print "No Data List Error"
        else:
            print "No Outputs List Error"
    else:
        print "Response Code Error"