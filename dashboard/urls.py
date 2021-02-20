from django.urls import path
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CookListView, AddCookView, HomeView, cookDetail, VacancyListView, JobView, CookSettingsView, JobSettingsView, UserSettingsView, LoginView, LogoutView, SignupView, UserUpdateView


urlpatterns = [
    url(r'^add_cook', AddCookView.as_view(), name="add_cook_url"),
    url(r'^add_job', JobView.as_view(), name="add_job_url"),
    url(r'^cooklist', CookListView.as_view(), name="cooklist_url"),
    url(r'^cook_job', VacancyListView.as_view(), name="cook_job_url"),
    path('cookdetails/<int:cook_id>/', cookDetail, name='cookdetails_url'),
    path('', HomeView.as_view(), name="home_url"),
    url(r'^user_settings', UserSettingsView.as_view(), name="user_settings_url"),
    url(r'^cook_settings', CookSettingsView.as_view(), name="cook_settings_url"),
    url(r'^job_settings', JobSettingsView.as_view(), name="job_settings_url"),
    url(r'^login', LoginView.as_view(), name="login_url"),
    url(r'^signup', SignupView.as_view(), name="signup_url"),
    url(r'^logout', LogoutView.as_view(), name="logout_url"),
    url(r'^user_update', UserUpdateView.as_view(), name="user_update_url"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
