# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views.generic import View

import json

from .models import Post

# Create your views here.

class PostsList(View):    
    def get(self, req):
        # Get posts
        posts = Post.objects.all()

        # Render posts
        return render(req, 'blog/posts_list.html', context = {
            'posts': posts
        })
    # end
# end

class ViewPost(View):
    def get(self, req, id):
        post = get_object_or_404(Post, id = id)

        comments = list(post.comments.all())

        for ma in range(post.comments.count()):
            likes = json.loads(comments[ma].likes)['likes']

            print(len(likes))
            comments[ma].likesInt = len(likes)
            comments[ma].isLiked = "1" in likes

        return render(req, 'blog/post.html', context = {
            'post': post,
            'comments': comments
        })
    # end
# end
