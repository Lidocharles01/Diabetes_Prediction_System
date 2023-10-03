from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='index'),

    path('register', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('user_home', views.user_home, name='user_home'),
    path("predict/", views.predict),
    path("predict/result", views.result),

]
