# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.http import HttpResponse

from django.conf import settings
from django.core.files.storage import FileSystemStorage

import random
import json

from .models import Post, Author

# Create your views here.

'''
    ### RESPONSE ###
    200 - Success
    400 - Requested resource wan't found
    500 - Session wasn't confirmed
'''

class LoginView(View):
    def get(self, request):
        if(not request.session.get('uauth', False)): # no auth data -> move to login page
            return render(request, 'blog/login.html')
        else: # already logined -> move to home page
            return redirect('view_posts_url')
    # end

    def post(self, request):
        # Get body
        data = json.loads(request.body)
        success = False

        def _response(status):
            return HttpResponse(json.dumps({
                'status': status
            }))
        # end

        if(not request.session.get('uauth', False)): request.session['uauth'] = {}

        try:
            user = Author.objects.get(login = data['login'], password = data['password'])
            # breaks here if user doesn't exist
            request.session['uauth']['login'] = user.login

            return _response(200)
        except Author.DoesNotExist:
            return _response(400)
        # end
    # end
# end

class RegisterView(View):
    def get(self, request):
        if(not request.session.get('uauth', False)): # no auth data -> move to register page
            return render(request, 'blog/register.html')
        else: # already logined -> move to home page
            return redirect('view_posts_url')
    # end

    def post(self, request):
        # Get body
        data = json.loads(request.body)
        resolved = False

        if(not request.session.get('uauth', False)): request.session['uauth'] = {}

        def submit(status):
            resolved = True
            return HttpResponse(json.dumps({
                'status': status
            }))

        # Check if user with login exists
        try:
            Author.objects.get(login = data['login'])
            return submit(400)
        except Author.DoesNotExist:
            # Create user
            user = Author()
            user.login = request.session['uauth']['login'] = data['login']
            user.password= data['password']
            user.name = data['name']
            user.save()

            # Submit success response
            if(not resolved): return submit(200)
        # end
    # end
# end

class LogoutView(View):
    def get(self, request):
        if(request.session.get('uauth', False)):
            request.session['uauth'] = None
        # end
        return redirect('login_page_url')
    # end
# end

class PostsList(View):    
    def get(self, request):
        # Get posts
        posts = Post.objects.all()

        # Render posts
        return render(request, 'blog/posts_list.html', context = {
            'posts': posts
        })
    # end
# end

class ViewPost(View):
    def get(self, request, id):
        post = get_object_or_404(Post, id = id)

        return render(request, 'blog/post.html', context = {
            'post': post
        })
    # end
# end

class WriteView(View):
    def get(self, request):
        # Check if user has a session
        if(request.session['uauth']): # Return page if user authenticated
            return render(request, 'blog/newpost.html')
        else: # User has no session -> Move to login page
            return redirect('login_page_url')
        # end
    # end
    
    def post(self, request):
        '''
            Check if user has his session (Doesn't make any sense,
            because we're checking session in GET request resolver and user cannot
            do a POST request from an other client (postman for example),
            because django validates csrftoken).
        '''

        def _response(status):
            return HttpResponse(json.dumps({
                'status': status
            }))
        # end

        if(not request.session['uauth']): return _response(500)
        
        # Get data
        data = json.loads(request.POST.get('data'))

        try:
            user = Author.objects.get(login = request.session['uauth']['login'])
        except Author.DoesNotExist: # session was not confirmed
            return _response(500)
        # end
    
        # TODO: Image
        def genFName():
            a = list("abcdefghijklmnopqrstuvwxyz")
            b = ""

            for ma in range(100):
                b += random.choice(a)
            # end

            return request.session['uauth']['login'] + "_" + b
        # end

        # Receive image
        image = request.FILES['image']
        fs = FileSystemStorage()
        imageFS_Filename = fs.save(genFName(), image)
        imageUrl = fs.url(imageFS_Filename)

        np = Post()
        np.title = data['title']
        np.content = data['content']
        np.image = imageUrl
        np.likes = '{"likes":[]}' # Empty JSON object
        np.save()

        np.author.add(user)

        return _response(200)
    # end
# end