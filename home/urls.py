from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('logout/', views.logout_, name='logout'),
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('profile/', views.MyProfile.as_view(),name='profile')
]

