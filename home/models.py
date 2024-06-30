from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Create your models here.


class CustomUser(AbstractUser):
    
    profile_pic = models.ImageField(_('Profile Picture'), upload_to='profile_img/',blank=True, default='/profile_img/standard.png')
    birth_date = models.DateField(_('Birth Date'), null=True,blank=True)
    phone = models.CharField(_('Phone Number'), max_length=15,help_text='Type your number')
    description = models.TextField(_('Description'), max_length=600, blank=True, null=True)
    city = models.CharField(max_length=70, blank=True, null=True)
    job = models.ManyToManyField('Job', related_name='users')
    genre = models.ForeignKey('Genre', related_name='users', on_delete=models.SET_NULL, null=True,blank=True)
    price_average = models.FloatField(_('Price Average'), blank=True, null=True)
    is_contractor = models.BooleanField(_('Is Contractor'), default=True, help_text='Check this box if you want hire a job instead make a freelancer')
    email = models.EmailField('E-mail')
    
    
    brazil_states = (
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'))
    
    uf = models.CharField(max_length=2, choices=brazil_states, help_text='Select the state where you live', blank=True,null=True)
    
    def get_absolute_url(self):
        return reverse("user-detail", args=[str(self.id)])
    
    class Meta:
        ordering = ['price_average']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    
    

class Job(models.Model):
    
    JOB_ROLES = (
        ('Electrician', 'Electrician'),
        ('Cook', 'Cook'),
        ('Carpenter', 'Carpenter'),
        ('Blacksmith', 'Blacksmith'),
        ('Driver', 'Driver'),
        ('Babysitter', 'Babysitter'),
        ('Cleaner', 'Cleaner'),
        ('Mechanic', 'Mechanic'),
        ('Manual Work', 'Manual Work'),
    )
    
    
    
    name = models.CharField(_('Job'),max_length=11 ,choices=JOB_ROLES)
    
    def __str__(self):
        return self.name
    
    
class Genre(models.Model):
    
    OPTIONS = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('O', 'Other'),
        )
    
    option = models.CharField(_('Genre'),max_length=1 ,choices=OPTIONS)
    
    def __str__(self):
        return self.option
    
    

class Proposal(models.Model):
    
    title = models.CharField(_('Title'), max_length=40, blank=False)
    details = models.CharField(_('Details'), max_length=600, blank=False)
    contractor = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='proposals')


    def get_absolute_url(self):
        return reverse("proposal-detail", args=[str(self.id)])
    