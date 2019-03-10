from django.conf.urls import url

from .views import PostsList, ViewPost

urlpatterns = [
    url(r'^$', PostsList.as_view(), name = 'view_posts_url'),
    url(r'^post/(?P<id>\w+)$', ViewPost.as_view(), name = 'view_post_url')
]