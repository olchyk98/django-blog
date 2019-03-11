from django.conf.urls import url

from .views import PostsList, ViewPost, LoginView, RegisterView

urlpatterns = [
    url(r'^$', PostsList.as_view(), name = 'view_posts_url'),
    url(r'^post/(?P<id>\w+)$', ViewPost.as_view(), name = 'view_post_url'),
    url(r'^login/$', LoginView.as_view(), name = 'login_page_url'),
    url(r'^register/$', RegisterView.as_view(), name = 'register_page_url')
]