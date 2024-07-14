from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('logout/', views.logout_, name='logout'),
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('profile/', views.MyProfile.as_view(),name='profile'),
    path('profile/edit', views.edit_profile,name='profile-edit'),
    path('profile/<int:pk>/', views.ProfileDetail.as_view(),name='user-detail'),
    path('proposal/create/<int:freelancer_id>/', views.ProposalCreate.as_view(), name='proposal-create'),
    path('profile/proposals/', views.AcProposalList.as_view(),name='proposal-list'),
]

