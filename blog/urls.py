from django.conf.urls import url

from .views import PostsList

urlpatterns = [
    url(r'^$', PostsList.as_view())
]