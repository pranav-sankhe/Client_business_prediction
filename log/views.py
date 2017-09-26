#!python
#log/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response 
from django.http import HttpResponseRedirect 
from django.contrib.auth.forms import UserCreationForm 
import forms
from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
# this login required decorator is to not allow to any  
# view without authenticating
@login_required(login_url="login/")
def home(request):
	return render(request,"home.html")


def register_page(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],email=form.cleaned_data['email'])
            return HttpResponseRedirect('/')
    form = forms.RegistrationForm()
    #variables = RequestContext(request, {'form': form})
    return render(request,'/home/pranav/Documents/django-auth-pattern/templates/register.html', {'form': form})