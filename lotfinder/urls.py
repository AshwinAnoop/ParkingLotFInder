from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('login',views.login, name='login'),
    path('signup',views.signup, name='signup'),
    path('monthlyhome',views.monthlyhome, name='monthlyhome'),
    path('logout',views.logout, name='logout'),
    path('myspacehome',views.myspacehome, name='myspacehome'),
    path('addparking',views.addparking, name='addparking'),
]