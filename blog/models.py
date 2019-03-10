# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# POST: title, image, content, previewcontent, author {}, comments {}, date
# USER: avatar, name, description, login, password
# COMMENT: author {}, content, date, likes

class Post(models.Model):
    title = models.CharField(max_length = 400)
    image = models.CharField(max_length = 300)
    content = models.TextField()
    date = models.DateField(auto_now_add = True)
    likes = models.TextField() # JSON ids
    comments = models.ManyToManyField('Comment', blank = True, related_name = 'posts')
    author = models.ManyToManyField('User', blank = False, related_name = 'posts')

    def __str__(self):
        return self.title
    # end
# end

class User(models.Model):
    avatar = models.CharField(max_length = 300)
    name = models.CharField(max_length = 100)
    description = models.SlugField(max_length = 800)
    login = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)

    def __str__(self):
        return self.name
    # end
# end

class Comment(models.Model):
    content = models.TextField()
    date = models.DateField(auto_now_add = True)
    likes = models.TextField() # JSON ids
    author = models.ManyToManyField('User', blank = False, related_name = 'comments')

    def __str__(self):
        return self.content[:10]
