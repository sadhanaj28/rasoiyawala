from django.urls import path
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import DashboardView, AddCookView

urlpatterns = [
    # url(r'^dashboard', DashboardView.as_view(), name="dashboard_url"),
    url(r'^add_cook', AddCookView.as_view(), name="add_cook_url"),
    path('', DashboardView.as_view(), name="dashboard_url"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
