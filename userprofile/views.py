from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import SingForm
from .models import Userprofile

from team.models import Team

def singup(request):
    if request.method == "POST":
        form = SingForm(request.POST)
        if form.is_valid():
            user = form.save()

            
            team = Team.objects.create(name="The team name", created_by=user)
            team.members.add(user)
            team.save()

            Userprofile.objects.create(user=user, active_team=team)

            return redirect('/log-in/')
    else:
        form = SingForm()

    return render(request, 'userprofile/singup.html', {
        'form':form
    })

@login_required
def myaccount(request):
    return render(request, 'userprofile/myaccount.html')