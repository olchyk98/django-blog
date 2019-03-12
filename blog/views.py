# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.http import HttpResponse

import json

from .models import Post, Author

# Create your views here.

class LoginView(View):
    def get(self, request):
        if(not request.session['uauth']): # no auth data -> move to login page
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
            request.session['uauth']['password'] = user.password

            return _response(200)
        except Author.DoesNotExist:
            print("Doesn't exist")
            return _response(400)
        # end
    # end
# end

class RegisterView(View):
    def get(self, request):
        if(not request.session['uauth']): # no auth data -> move to register page
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
        if(Author.objects.get(login = data['login'])):
            return submit(400)

        # Create user
        user = Author()
        user.login = request.session['uauth']['login'] = data['login']
        user.password = request.session['uauth']['password'] = data['password']
        user.name = data['name']
        user.save()

        # Submit success response
        if(not resolved): return submit(200)
    # end
# end

class LogoutView(View):
    def get(self, request):
        request.session['uauth'] = None
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

        comments = list(post.comments.all())

        for ma in range(post.comments.count()):
            likes = json.loads(comments[ma].likes)['likes']

            comments[ma].likesInt = len(likes)
            comments[ma].isLiked = "1" in likes

        return render(request, 'blog/post.html', context = {
            'post': post,
            'comments': comments
        })
    # end
# end
