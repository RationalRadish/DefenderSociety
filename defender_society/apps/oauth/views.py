from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm
from django.contrib import messages
import os
# Create your views here.

@login_required
def profile_view(request):
    return render(request,'oauth/profile.html')

@login_required
def change_profile_view(request):
    if request.method =='POST':
        old_avatar_file = request.user.avatar.path
        old_avatar_url = request.user.avatar.url
        # Upload files need to use request.FILES
        form = ProfileForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            if not old_avatar_url =='/media/avatar/default.png':
                if os.path.exists(old_avatar_file):
                    os.remove(old_avatar_file)
            form.save()
            # Add a message and redirect to the personal information page if the form is successfully verified
            messages.add_message(request,messages.SUCCESS,'The personal information was updated successfully!')
            return redirect('oauth:profile')
    else:
        # Return an empty form if it is not a POST request
        form = ProfileForm(instance=request.user)
    return render(request,'oauth/change_profile.html',context={'form':form})