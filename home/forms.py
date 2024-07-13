from django.contrib.auth.forms import UserCreationForm
from home.models import CustomUser
from django import forms
from home.models import Proposal

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'first_name', 'last_name', 'genre','is_contractor',
            'profile_pic','birth_date','phone','description',
            'uf','city','job','price_average','email'
        )
        
        widgets = {
            'description':forms.Textarea(attrs={'rows':3,'cols':40}),
            'birth_date' : forms.DateInput(attrs={'type':'date','class':'date-input'})
        }
        
    
class ProposalForm(forms.ModelForm):
    
    class Meta:
        model = Proposal
        fields = ['title','details']
        
        
class EditProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser
