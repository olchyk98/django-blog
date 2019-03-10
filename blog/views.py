# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View

from django.http import HttpResponse

# Create your views here.

class PostsList(View):
    def get(self, req):
        return render(req, 'blog/posts_list.html', context = {
            'posts': []
        })
