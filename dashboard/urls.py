from django.urls import path
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CookListView, AddCookView, HomeView


urlpatterns = [
    url(r'^add_cook', AddCookView.as_view(), name="add_cook_url"),
    path('^cooklist', CookListView.as_view(), name="cooklist_url"),
    path('', HomeView.as_view(), name="home_url"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
