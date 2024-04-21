from django.views.generic import TemplateView
from django.shortcuts import render
from api.models.userModel import UserModel
from api.models.jobModel import JobModel
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Q
from api.models.applyJobModel import ApplyJobModel

class EmployeeRegistrationView(TemplateView):
    template_name = "employee/registration.html"
    def post(self, request):
        password = request.POST["password"]
        data = {
            "username": request.POST["username"],
            "email": request.POST["email"],
            "role": 1
        }
        if password == request.POST["confirm_password"]:
            user = UserModel.objects.create(**data)
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(reverse("employee_login"))
        else:
            messages.error(request, "Password not matching")
            return render(request, self.template_name)    
        
class LoginView(TemplateView):
    template_name = "employee/login.html"
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("employee_homepage"))
        else:
            messages.error(request, "Invalid Credentials")
            return render(request, self.template_name)        
        
class HomepageView(TemplateView):
    template_name = "employee/homepage.html"
    def get(self, request):
        user = request.user
        return render(request, self.template_name, locals())
    def post(self, request):
        title = request.POST["title"]
        location = request.POST["location"]
        company_name = request.POST["company_name"]
        experience = [int(request.POST["experience"][0])] if int(request.POST["experience"][0]) != 0 else [0,1,2,3,4,5]
        filters = Q()
        if location:
            filters &= Q(location__icontains = location)
        if company_name:
            filters &= Q(employer__company_name__icontains = company_name)
        if title:
            filters &= Q(title__icontains = title)
        filters &= Q(experience__in = experience)    
        filter_jobs = JobModel.objects.filter(filters)
        print(filter_jobs, '=======')
        return render(request, self.template_name, locals())
    
class ViewJobDescriptionView(TemplateView):
    template_name = "employee/viewJob.html"
    def get(self, request, job_id):
        job = JobModel.objects.get(id = job_id)
        return render(request, self.template_name, locals())
    
class ApplyJobView(TemplateView):
    template_name = "employee/apply_job.html"
    def get(self, request, job_id):
        job = JobModel.objects.get(id = job_id)
        company = job.employer.company_name
        check_application = ApplyJobModel.objects.filter(employee_id = request.user.id, job_id = job_id).first()
        if check_application:
            return HttpResponse("You already applied for this job.")
        return render(request, self.template_name, locals())

    def post(self, request, job_id):
        data = {
            "phone_no": request.POST["phone_no"],
            "email": request.POST["email"],
            "resume": request.FILES["resume"],
            "job_id": job_id
        }
        apply_job = ApplyJobModel.objects.create(employee_id = request.user.id, **data)
        messages.info(request, "Application sent successfully.")
        return HttpResponseRedirect(reverse("employee_homepage"))