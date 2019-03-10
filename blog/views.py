# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from django.http import HttpResponse

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
