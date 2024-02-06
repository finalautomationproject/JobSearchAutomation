# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from .models import UserProfile, ScrapedJob, IndeedJob
from .forms import UserProfileForm
from .linkedin import EasyApplyLinkedin 
from .indeed import ScrapeIndeed
from .models import UserProfile  # Import the UserProfile model

def userinfo(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            # Check if the user already has a profile
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                # Update the existing profile with the new data from the form
                user_profile.email = form.cleaned_data['email']
                user_profile.linkedin_password = form.cleaned_data['linkedin_password']
                user_profile.indeed_password = form.cleaned_data['indeed_password']
                user_profile.keywords = form.cleaned_data['keywords']
                user_profile.location = form.cleaned_data['location']
                user_profile.resume = form.cleaned_data['resume']

                user_profile.save()
            except UserProfile.DoesNotExist:
                # If the user doesn't have a profile, create a new one
                user_profile = form.save(commit=False)
                user_profile.user = request.user
                user_profile.save()

            return redirect('search_jobs')  # Redirect to a success page or wherever you want
    else:
        # Check if the user already has a profile
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            # If a profile exists, populate the form with the existing data
            form = UserProfileForm(instance=user_profile)
        except UserProfile.DoesNotExist:
            # If the user doesn't have a profile, initialize an empty form
            form = UserProfileForm()

    return render(request, 'jobseeker/userinfo.html', {'form': form})



def searchjobs(request):
    userinfo = get_object_or_404(UserProfile, user=request.user)
    data = {
        'email': userinfo.email,
        'password': userinfo.linkedin_password,
        'keywords': userinfo.keywords,
        'location': userinfo.location
    }
    form = userinfo
    if request.method == 'POST':
        if 'Linkedinsearch' in request.POST:
            # Code to execute when LinkedIn Search button is clicked
            linkedin_search = EasyApplyLinkedin(data=data)
            # Perform LinkedIn search operation
            linkedin_search.apply()
            linkedin_search_results = linkedin_search.scrape_offers()
            for result in linkedin_search_results:
                title, company, location = result
                linkedin_job = ScrapedJob(job_title=title, company_name=company, job_description=location)
                linkedin_job.save()

            # Process search result or redirect to a page showing the result
            return redirect('scrapedjobs')  # Redirect to a view to display search result
        elif 'Indeedsearch' in request.POST:
            # Code to execute when Indeed Search button is clicked
            indeed_search = ScrapeIndeed(data=data)
            indeed_search.search_jobs()
            # Perform Indeed search operation
            indeed_search_result = indeed_search.job_results()
            for jobinfo in indeed_search_result:
                job_object = IndeedJob(jobinfo=jobinfo)
                job_object.save()

            # Process search result or redirect to a page showing the result
            return redirect('scrapedjobs')  # Redirect to a view to display search result

    return render(request, 'jobseeker/searchjobs.html', {'form': form})

def scrapedjobs(request):
    scraped_jobs = ScrapedJob.objects.all()
    indeed_jobs = IndeedJob.objects.all()
    for object in indeed_jobs:
        if object == "":
            object.delete()
        
    return render(request, 'jobseeker/scrapedjobs.html', {'scraped_jobs': scraped_jobs, 'indeed_job': indeed_jobs})

def home(request):

    return render(request, 'jobseeker/home.html')


def logout_view(request):
    logout(request)
    return redirect('login')
