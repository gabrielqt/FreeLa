from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponse
from home.models import CustomUser, Proposal
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from home.forms import CustomUserCreationForm, ProposalForm, EditProfileForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

# Create your views here.

class Home (ListView):
    
    model = CustomUser
    paginate_by = 9
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
    


class ProposalCreate(LoginRequiredMixin, CreateView):
    
    model = Proposal    
    form_class = ProposalForm
    template_name = 'proposal-create.html'

    def form_valid(self, form):
        
        freelancer_id = self.kwargs['freelancer_id']
        freelancer = get_object_or_404(CustomUser, pk=freelancer_id)
        form.instance.contractor = self.request.user
        form.instance.freelancer = freelancer
        
        response = super().form_valid(form) #salva o formulário
        
        messages.success(self.request, f'Proposal sent to {freelancer.first_name}')
        
        return response
        
    def get_success_url(self) -> str:
        freelancer_id = self.kwargs['freelancer_id']
        return reverse_lazy('user-detail', kwargs={'pk':freelancer_id})
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        freelancer_id = self.kwargs['freelancer_id']
        freelancer = get_object_or_404(CustomUser, pk=freelancer_id)
        context = super().get_context_data()
        context['freelancer'] = freelancer
        return context



class ProposalList(LoginRequiredMixin, ListView):
    
    model = Proposal
    template_name = 'proposal_list.html'
    context_object_name = 'proposals'
    paginate_by = 6
    
    def get_queryset(self):
        freelancer = self.request.user
        status = self.kwargs.get('status')
        return Proposal.objects.filter(freelancer=freelancer.id, status=status)
    



class ProposalDetail(LoginRequiredMixin, DetailView):
    
    model = Proposal
    template_name = 'proposal-detail.html'
    context_object_name = 'proposal'
    

@login_required
def delete_proposal(request, pk):
    
    proposal = get_object_or_404(Proposal, pk=pk)
    
    if request.user == proposal.freelancer or proposal.contractor:
        proposal.delete()
        messages.success(request,'Proposta finalizada.')
    else:
        messages.success(request,'Proposta não finalizada.')
    
    return redirect('profile')

@login_required
def accept_proposal(request, pk):
    
    proposal = get_object_or_404(Proposal, pk=pk)
    
    if proposal.freelancer == request.user:
        proposal.status = 'accepted'
        proposal.save()
        messages.success(request,'Proposal accepted.')
    
    return redirect('profile')


class Search(ListView):
    
    model = CustomUser
    template_name = 'search.html'
    context_object_name = 'users'

    def get_queryset(self) -> QuerySet[Any]:
        
        query = self.request.GET.get('q')
        if query:
            return CustomUser.objects.filter(job__name__iexact =query) | CustomUser.objects.filter(city__iexact=query) | CustomUser.objects.filter(first_name__icontains=query) | CustomUser.objects.filter(description__icontains= query)
        else:
            return CustomUser.objects.filter(is_contractor=False)

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



class MyProfile(LoginRequiredMixin,DetailView):
    
    model = CustomUser
    template_name = 'registration/profile.html'
    context_object_name = 'user'
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return self.request.user
    
class ProfileDetail(LoginRequiredMixin,DetailView):
    
    model = CustomUser
    template_name = 'registration/profile-detail.html'
    context_object_name = 'user'
    

def edit_profile(request):
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    
            
    return render(request, 'registration/edit-profile.html', context={'form':form, 'user':request.user})
        