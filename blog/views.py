# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import HttpResponse

import json

from .models import Post, Author

# Create your views here.

class LoginView(View):
    def get(self, request):
        return render(request, 'blog/login.html', context = {

        })
    # end
# end

class RegisterView(View):
    def get(self, request):
        return render(request, 'blog/register.html', context = {

        })
    # end

    def post(self, request):
        # Get body
        data = json.loads(request.body)
        resolved = False

        if(not request.user): request.user = {}

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
        user.login = request.user['login'] = data['login']
        user.password = request.user['password'] = data['password']
        user.name = data['name']
        user.save()

        # Submit success response
        if(not resolved): return submit(200)
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
