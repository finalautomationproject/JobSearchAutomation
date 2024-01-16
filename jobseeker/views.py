# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import LinkedInForm  # Assuming you have a form for user input
from .linkedin import EasyApplyLinkedin  # Import your automation script

def linkedin(request):
    if request.method == 'POST':
        form = LinkedInForm(request.POST)
        if form.is_valid():
            # Get user data from the form
           cleandata = form.cleaned_data
           
            
        data = {
            'email': cleandata.email,
            'password': cleandata.linkeInPass,
            'keywords': ['python', 'django', 'automation'],
            'location': 'Nairobi, Kenya'
            }


            # Initialize your automation script with user data
        bot = EasyApplyLinkedin(data)
        bot.apply()

            # You can pass the result or any other data to the template
           # return render(request, 'application_result.html', {'result': result})

    else:
        form = LinkedInForm()

    return render(request, 'jobseeker/linkedinapply.html', {'form': form})

def home(request):
    return render(request, 'jobseeker/home.html')


def logout_view(request):
    logout(request)
    return redirect('login')
