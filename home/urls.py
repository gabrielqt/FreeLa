from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('logout/', views.logout_, name='logout'),
    path('login/', views.login_page, name='login')
]

