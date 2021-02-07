from django.urls import path
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CookListView, AddCookView, HomeView, cookDetail, VacancyListView, JobView


urlpatterns = [
    url(r'^add_cook', AddCookView.as_view(), name="add_cook_url"),
    url(r'^add_job', JobView.as_view(), name="add_job_url"),
    path('^cooklist', CookListView.as_view(), name="cooklist_url"),
    path('^vacancylist', VacancyListView.as_view(), name="vacancylist_url"),
    path('cookdetails/<int:cook_id>/', cookDetail, name='cookdetails_url'),
    path('', HomeView.as_view(), name="home_url"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
