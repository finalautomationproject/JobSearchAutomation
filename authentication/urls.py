from django.urls import path, include
from . import views


urlpatterns = [             
    path('register', views.register, name="register"),
    path('login/', views.login_user, name="login"),
    path('', views.login_user, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('jobseeker/userinfo/', views.jobseeker_home_view, name='jobseeker-home'),

]
