from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from accounts.models import Profile

# __author__ = 'ipman'


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


@login_required
def index(request):
    if Profile.objects.get(user=request.user).mobile_version:
        return redirect('mobile:getlist-executor-tasks')
    return render(request, 'dashboard.html', {
        'user': request.user,
    })
