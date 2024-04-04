# views.py
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from .models import UserProfile, ScrapedJob, IndeedJob, DiceJob, NaukriJob, ZipRecruiterJob, AllJobs, JobSearchErrors, JobSuccess
from .forms import UserProfileForm
from mammoth import convert_to_html
from .scrapingscripts import ScrapeIndeed, DiceApp, ZipRecruiterApp, NaukriApp, EasyApplyLinkedin
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
                success = JobSuccess(user= request.user, success_instance="User Information Saved")
                success.save()
                return redirect('search_jobs')  
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
        'country': userinfo.country,
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
            success = JobSuccess(user= request.user, success_instance=f"{job_title} scraped")
            success.save()

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
                success = JobSuccess(user= request.user, success_instance=f"{job_title} scraped")
                success.save()
    def dicesearch():
            dice_search = DiceApp(data=data)
            dice_search.job_search()
            dice_search_results = dice_search.extract_jobs()
            for jobinfo in dice_search_results:
                title = jobinfo['title']
                company = jobinfo['company']
                location = jobinfo['location']
                description = jobinfo['description']
                employment_type = jobinfo['employment_type']
                posted_date = jobinfo['posted_date']
                application_url = jobinfo['application_url']
                job_object = DiceJob(title=title, company=company, location=location, description=description, employment_type=employment_type, posted_date=posted_date, application_url=application_url)
                all_jobs = AllJobs(application_website="Dice", job_title=title, company=company, application_url=application_url)
                all_jobs.save()
                job_object.save()
                success = JobSuccess(user= request.user, success_instance=f"{title} scraped")
                success.save()
    def naukrisearch():
            naukri_search = NaukriApp(data=data)
            naukri_search.job_search()
            naukri_search_results = naukri_search.extract_jobs()
            for jobinfo in naukri_search_results:
                title = jobinfo['title']
                company = jobinfo['company']
                experience = jobinfo['experience']
                description = jobinfo['description']
                tags_list = jobinfo['tags_list']
                posting_date = jobinfo['posting_date']
                application_url= jobinfo['application_url']
                job_object = NaukriJob(title=title, company=company, experience=experience, description=description, tags_list=tags_list, posting_date=posting_date, application_url=application_url)
                all_jobs = AllJobs(application_website="Naukri", job_title=title, company=company, application_url=application_url)
                all_jobs.save()
                success = JobSuccess(user= request.user, success_instance=f"{title} scraped")
                success.save()
                
                job_object.save()
    def ziprecruitersearch():
            ziprecruiter_search = ZipRecruiterApp(data=data)
            ziprecruiter_search.job_search()
            ziprecruiter_search_results = ziprecruiter_search.extract_jobs()
            for jobinfo in ziprecruiter_search_results:
                job_title = jobinfo['job_title']
                company = jobinfo['company']
                location = jobinfo['location']
                description = jobinfo['description']
                application_url = jobinfo['application_url']
                job_object = ZipRecruiterJob(job_title=job_title, company=company, location=location, description=description, application_url=application_url)
                all_jobs = AllJobs(application_website= "ZipRecruiter", job_title=job_title, company=company, application_url=application_url)
                all_jobs.save()
                job_object.save()
                success = JobSuccess(user= request.user, success_instance=f"{job_title} scraped")
                success.save()
    if request.method == 'POST':
        if 'Linkedinsearch' in request.POST:
            try:
                naukrisearch()
            except Exception as e:
                error = JobSearchErrors(user = request.user, error_instance='LinkedIn Search', error=e)
                error.save()
                print("Could not complete search:"+ e)    

        elif 'Indeedsearch' in request.POST:
            try:
                indeedsearch()
            except Exception as e:
                error = JobSearchErrors(user = request.user, error_instance='Indeed Search', error=e)
                error.save()
                print("Could not complete search:"+ e)
        elif 'Dicesearch' in request.POST:
            try:
                dicesearch()
            except Exception as e:
                error = JobSearchErrors(user = request.user, error_instance='Dice Search', error=e)
                error.save()
                print("Could not complete search:"+ e)
        elif 'Naukrisearch' in request.POST:
            try:
                naukrisearch()
            except Exception as e:
                error = JobSearchErrors(user = request.user, error_instance='Naukri Search', error=e)
                error.save()
                print("Could not complete search:"+ e)
        elif 'ZipRecruitersearch' in request.POST:
            try:
                ziprecruitersearch()
            except Exception as e:
                error = JobSearchErrors(user=request.user.id, error_instance='ZipRecruiter Search', error=e)
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
                error = JobSearchErrors(user=request.user, error_instance='AllWebsiteSearch', error=e)
                error.save()
                print("Could not complete searches:", e)
                return redirect('scrapedjobs')

        return redirect('scrapedjobs')  # Redirect to a view to display search result

    return render(request, 'jobseeker/searchjobs.html', {'form': form})

def scrapedjobs(request):
    userinfo = get_object_or_404(UserProfile, user=request.user)
    data = {
        'email': userinfo.email,
        'password': userinfo.linkedin_password,
        'keywords': userinfo.interests,
        'location': userinfo.location
    }
    resume_file = userinfo.resume.path
    resume_path = os.path.abspath(resume_file)

    phone_number = userinfo.phone_number

    scraped_jobs = ScrapedJob.objects.all()
    indeed_jobs = IndeedJob.objects.all()
    ziprecruiter_jobs = ZipRecruiterJob.objects.all()
    naukri_jobs = NaukriJob.objects.all()
    dice_jobs = DiceJob.objects.all()
    if request.method == 'POST':
        if 'easyapply' in request.POST:
            dice_search = DiceApp(data=data)
            dice_search.login()
            for job in dice_jobs:
                try:
                    dice_search.easyApply(job.application_url)
                    success = JobSuccess(user= request.user.id, success_instance="Dice Automatic Application")
                    success.save()
                except Exception as e:
                    print("error in easyapply:", e)
                    return redirect('results')
            for job in scraped_jobs:
                linkedin_search = EasyApplyLinkedin(data=data)
                linkedin_search.login_linkedin()
                try:
                    linkedin_search.apply_to_job(phone_number, resume_path)
                    success = JobSuccess(user= request.user, success_instance="LinkedIn Automatic Application")
                    success.save()
                except Exception as e:
                    print("Error", e)
                    return redirect('results')
    for object in indeed_jobs:
        if object == "":
            object.delete()
    context = {'scraped_jobs': scraped_jobs, 'indeed_jobs': indeed_jobs, 'ziprecruiter_jobs': ziprecruiter_jobs,
                'naukri_jobs': naukri_jobs, 'dice_jobs': dice_jobs}    
    return render(request, 'jobseeker/scrapedjobs.html', context)

from django.shortcuts import render
from .models import JobSearchErrors, JobSuccess

def display_errors_and_success(request):
    # Retrieve JobSearchErrors and JobSuccess instances
    errors = JobSearchErrors.objects.all()
    successes = JobSuccess.objects.all()
    
    # Pass data to template for rendering
    context = {
        'errors': errors,
        'successes': successes,
    }
    
    # Render template with data
    return render(request, 'jobseeker/successanderrors.html', context)


def home(request):
    userinfo = get_object_or_404(UserProfile, user=request.user)
    alljobs = AllJobs.objects.all()
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

    context = {'userinfo': userinfo, 'html_content': html_content, 'avatar': avatar, 'alljobs': alljobs}
    return render(request, 'jobseeker/home.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')