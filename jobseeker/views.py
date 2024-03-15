# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from .models import UserProfile, ScrapedJob, IndeedJob, DiceJob, NaukriJob, ZipRecruiterJob, AllJobs, JobSearchErrors
from .forms import UserProfileForm
from mammoth import convert_to_html
from .indeed import ScrapeIndeed, DiceApp, ZipRecruiterApp, NaukriApp, EasyApplyLinkedin
from .models import UserProfile  # Import the UserProfile model


def userinfo(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            except UserProfile.DoesNotExist:
                form = UserProfileForm(request.POST, request.FILES)

            if form.is_valid():
                form.instance.user = request.user
                form.save()
                return redirect('search_jobs')  # Redirect to a success page or wherever you want
    else:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            form = UserProfileForm(instance=user_profile)
        except UserProfile.DoesNotExist:
            form = UserProfileForm()

    return render(request, 'jobseeker/userinfo.html', {'form': form})



def searchjobs(request):
    userinfo = get_object_or_404(UserProfile, user=request.user)
    data = {
        'email': userinfo.email,
        'password': userinfo.linkedin_password,
        'keywords': userinfo.interests,
        'location': userinfo.location
    }
    form = userinfo
    user = request.user
    def linkedinsearch():
        linkedin_search = EasyApplyLinkedin(data=data)
        # Perform LinkedIn search operation
        linkedin_search.apply()
        linkedin_search_results = linkedin_search.scrape_offers()
        for result in linkedin_search_results:
            job_title = result['job_title']
            company_name= result['company_name']
            location = result['location']
            url = result['url']

            linkedin_job = ScrapedJob(user=user, job_title=job_title, company_name=company_name, location=location, application_url=url)
            all_jobs = AllJobs.objects.create(application_website="LinkedIn", job_title=job_title, company=company_name, application_url=url)
            linkedin_job.save()
            all_jobs.save()

    def indeedsearch():
            # Code to execute when Indeed Search button is clicked
            indeed_search = ScrapeIndeed(data=data)
            indeed_search.search_jobs()
            # Perform Indeed search operation
            indeed_search_result = indeed_search.job_results()
            for jobinfo in indeed_search_result:
                job_title = jobinfo['job_title']
                company_name = jobinfo['company_name']
                location = jobinfo['location']
                job_description = jobinfo['job_description']
                application_url = jobinfo['application_url']
                job_object = IndeedJob(job_title=job_title, company_name=company_name, location=location, job_description=job_description, application_url=application_url)
                all_jobs = AllJobs(application_website="Indeed", job_title=job_title, company=company_name, application_url=application_url)
                all_jobs.save()                
                job_object.save()
    def dicesearch():
            dice_search = DiceApp(data=data)
            dice_search.job_search()
            dice_search_results = dice_search.extract_jobs()
            for jobinfo in dice_search_results:
                title,company, location, description, employment_type,posted_date,application_url = jobinfo
                job_object = DiceJob(title=title, company=company, location=location, description=description, employment_type=employment_type, posted_date=posted_date, application_url=application_url)
                all_jobs = AllJobs(application_website="Dice", job_title=title, company=company, application_url=application_url)
                all_jobs.save()
                job_object.save()
    def naukrisearch():
            naukri_search = NaukriApp(data=data)
            naukri_search.job_search()
            naukri_search_results = naukri_search.extract_jobs()
            for jobinfo in naukri_search_results:
                title = jobinfo[0]
                company = jobinfo[1]
                experience = jobinfo[2]
                description = jobinfo[3]
                tags_list = jobinfo[4]
                posting_date = jobinfo[5]
                application_url= jobinfo[6]
                job_object = NaukriJob(title, company, experience, description, tags_list, posting_date, application_url)
                all_jobs = AllJobs("Naukri", title, company, application_url)
                all_jobs.save()

                
                job_object.save()
    def ziprecruitersearch():
            ziprecruiter_search = ZipRecruiterApp(data=data)
            ziprecruiter_search.job_search()
            ziprecruiter_search_results = ziprecruiter_search.extract_jobs()
            for jobinfo in ziprecruiter_search_results:
                job_title = jobinfo[0]
                company = jobinfo[1]
                location = jobinfo[2]
                description = jobinfo[3]
                application_url = jobinfo[4]
                job_object = ZipRecruiterJob(request.user.id, job_title, company, location, description, application_url)
                all_jobs = AllJobs(user = request.user.id, application_website= "ZipRecruiter", job_title=job_title, company=company, application_url=application_url)
                all_jobs.save()
                job_object.save()
    if request.method == 'POST':
        if 'Linkedinsearch' in request.POST:

            linkedinsearch()

        elif 'Indeedsearch' in request.POST:

                indeedsearch()

        elif 'Dicesearch' in request.POST:

                dicesearch()

        elif 'Naukrisearch' in request.POST:
            try:
                naukrisearch()
            except Exception as e:
                error = JobSearchErrors(request.user.id, 'Naukri Search', e)
                error.save()
                print("Could not complete search:"+ e)
        elif 'ZipRecruitersearch' in request.POST:
            try:
                ziprecruitersearch()
            except Exception as e:
                error = JobSearchErrors(request.user.id, 'ZipRecruiter Search', e)
                error.save()
                print("Could not complete searches:"+ e)
        elif 'AllWebsiteSearch' in request.POST:
            try:
                linkedinsearch()
                indeedsearch()
                dicesearch()
                naukrisearch()
                ziprecruitersearch()
            except Exception as e:
                error = JobSearchErrors(request.user.id, 'AllWebsiteSearch', e)
                error.save()
                print("Could not complete searches:"+ e)

        return redirect('scrapedjobs')  # Redirect to a view to display search result

    return render(request, 'jobseeker/searchjobs.html', {'form': form})

def scrapedjobs(request):
    scraped_jobs = ScrapedJob.objects.all()
    indeed_jobs = IndeedJob.objects.all()
    ziprecruiter_jobs = ZipRecruiterJob.objects.all()
    naukri_jobs = NaukriJob.objects.all()
    dice_jobs = DiceJob.objects.all()
    for object in indeed_jobs:
        if object == "":
            object.delete()
    context = {'scraped_jobs': scraped_jobs, 'indeed_jobs': indeed_jobs, 'ziprecruiter_jobs': ziprecruiter_jobs,
                'naukri_jobs': naukri_jobs, 'dice_jobs': dice_jobs}    
    return render(request, 'jobseeker/scrapedjobs.html', context)

def home(request):
    userinfo = get_object_or_404(UserProfile, user=request.user)
    try:
        avatar = userinfo.avatar.url
    except:
        avatar = 'default.svg'
    try:
        with userinfo.resume.open() as file:
            result = convert_to_html(file)
            html_content = result.value
    except: 
        html_content = "No Resume Uploaded"
    context = {'userinfo': userinfo, 'html_content': html_content, 'avatar': avatar}
    return render(request, 'jobseeker/home.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')
