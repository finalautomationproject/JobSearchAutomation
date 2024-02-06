from . import views
from django.urls import path

urlpatterns = [             
    path('home', views.home, name="home"),
    path('userinfo', views.userinfo, name="userinfo"),
    path('logout/', views.logout_view, name="logout"),
    path('searchjobs', views.searchjobs, name="search_jobs"),
    path('scrapedjobs', views.scrapedjobs, name="scrapedjobs"),
   # path('jobseeker/home/', views.jobseeker_home_view, name='jobseeker-home'),

]
