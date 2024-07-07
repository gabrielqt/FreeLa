from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponse
from home.models import CustomUser
from django.views.generic import ListView, DetailView
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from home.forms import CustomUserCreationForm
# Create your views here.

class Home (ListView):
    
    model = CustomUser
    paginate_by = 10
    template_name = 'home.html'
    context_object_name = 'users'

    '''Interessante utilizar query set quando você precisar filtrar
    na List View'''
    def get_queryset(self) -> QuerySet[Any]:
        return CustomUser.objects.filter(is_contractor=False)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data()
        context['user'] = self.request.user
        return context
    
    


''' Authenticate Views:'''

def login_page(request):
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request=request, user=user)
                return redirect('home')
            else:
                messages.error(request, 'Please insert correct username and password.')
        else:
            messages.error(request, 'Please insert correct username and password.')
    else:
        form = AuthenticationForm()
        
    return render(request,'login.html', context={'form':form} )



def signup_page(request):
    


    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request=request,user=user)
            return redirect('home')
        else:
            messages.error(request,'Please fill the fields correctly.')
            
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', context={'form':form})
        

def logout_(request):
    
    logout(request)
    
    return redirect('home')



class MyProfile(DetailView, LoginRequiredMixin):
    
    model = CustomUser
    template_name = 'registration/profile.html'
    context_object_name = 'user'
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return self.request.user
    
class ProfileDetail(DetailView, LoginRequiredMixin):
    
    model = CustomUser
    template_name = 'registration/profile-detail.html'
    context_object_name = 'user'
    