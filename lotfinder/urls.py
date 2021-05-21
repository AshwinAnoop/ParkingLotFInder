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
    path('emp',views.employeelogin, name='emp'),
    path('employeehome',views.employeehome, name='employeehome'),
    path('editlisting/',views.editlisting, name='editlisting'),
    path('acceptrequest/',views.acceptrequest, name='acceptlisting'),
    path('commiting/',views.commiting, name='commiting'),
]