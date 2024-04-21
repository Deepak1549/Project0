from django.views.generic import TemplateView
from django.shortcuts import render
from api.models.userModel import UserModel
from api.models.jobModel import JobModel
from api.models.applyJobModel import ApplyJobModel
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from api.utils.sendMail import send_mail
from threading import Thread

class EmployerRegistrationView(TemplateView):
    template_name = "employer/registration.html"
    def post(self, request):
        password = request.POST["password"]
        data = {
            "username": request.POST["username"],
            "email": request.POST["email"],
            "company_name": request.POST["company_name"],
            "company_picture": request.FILES.get("company_picture"),
            "role": 2
        }
        if password == request.POST["confirm_password"]:
            user = UserModel.objects.create(**data)
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(reverse("employer_login"))
        else:
            messages.error(request, "Password not matching")
            return render(request, self.template_name)    
        
class LoginView(TemplateView):
    template_name = "employer/login.html"
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("employer_homepage"))
        else:
            messages.error(request, "Invalid Credentials")
            return render(request, self.template_name)
        
class HomepageView(TemplateView):
    template_name = "employer/homepage.html"
    def get(self, request):
        user = request.user
        jobs_listing = JobModel.objects.filter(employer = user.id)
        return render(request, self.template_name, locals())
    def post(self, request):
        if request.user.is_authenticated:
            # experience = [int(request.POST["experience"][0])] if int(request.POST["experience"][0]) != 0 else 
            print(request.POST, '---------')
            data = {
                "employer_id": request.user.id,
                "title": request.POST["title"],
                "description": request.POST["description"],
                "location": request.POST["location"],
                "experience": request.POST["experience"],
                "contact_us": request.POST["contact_us"],
            }
            post_job = JobModel.objects.create(**data)
            return HttpResponseRedirect(reverse("employer_homepage"))
        else:
            return HttpResponse("You don't have permission")
        
class ViewApplication(TemplateView):
    template_name = "employer/viewApplications.html"
    def get(self, request, job_id):
        applicants = ApplyJobModel.objects.filter(job_id = job_id).order_by("status")
        return render(request, self.template_name, locals())
    
class AcceptApplicationView(TemplateView):
    def get(self, request, application_id):
        appl_id = ApplyJobModel.objects.get(id = application_id)
        appl_id.status = 2
        appl_id.save()
        Thread(target=send_mail, args=[1, appl_id.email]).start()
        return HttpResponseRedirect(reverse("view_applications", args=[appl_id.job_id]))

class RejectApplicationView(TemplateView):
    def get(self, request, application_id):
        appl_id = ApplyJobModel.objects.get(id = application_id)
        appl_id.status = 3
        appl_id.save()
        Thread(target=send_mail, args=[2, appl_id.email]).start()
        return HttpResponseRedirect(reverse("view_applications", args=[appl_id.job_id]))