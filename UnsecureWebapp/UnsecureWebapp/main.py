from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from quests.models import UserProgress

def sign_in(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Line below shouldn't exist
            print("User " + user.username + " succesfully signed up with password " + form.data['password1'])
            UserProgress.objects.create(user=user)
            return HttpResponseRedirect('/')
        return render(request, 'signin.html', {'form': UserCreationForm()})
    else:
        return render(request, 'signin.html', {'form': UserCreationForm()})

def log_in(request):
    return render(request, 'login.html')

def index(request):
    return render(request, 'main.html')
