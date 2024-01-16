from . import views
from django.urls import path

urlpatterns = [             
    path('home', views.home, name="home"),
    path('linkedin', views.linkedin, name="linkedin"),
    path('logout/', views.logout_view, name="logout"),
   # path('jobseeker/home/', views.jobseeker_home_view, name='jobseeker-home'),

]
