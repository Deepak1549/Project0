from django.urls import path
from api.views import employeeView, employerView, landingPageView

urlpatterns = [
    ##LANDING PAGE
    path("landing-page/", landingPageView.LandingPageView.as_view(), name = "landing_page"),

    ## EMPLOYEE
    path("employee/registration/", employeeView.EmployeeRegistrationView.as_view(), name = "employee_registration"),
    path("employee/login/", employeeView.LoginView.as_view(), name = "employee_login"),
    path("employee/homepage/", employeeView.HomepageView.as_view(), name = "employee_homepage"),
    path("job-details/<int:job_id>/", employeeView.ViewJobDescriptionView.as_view(), name = "job_details"),
    path("apply-job/<int:job_id>/", employeeView.ApplyJobView.as_view(), name = "apply_job"),

    ## EMPLOYER
    path("employer/registration/", employerView.EmployerRegistrationView.as_view(), name = "employer_registration"),
    path("employer/login/", employerView.LoginView.as_view(), name = "employer_login"),
    path("employer/homepage/", employerView.HomepageView.as_view(), name = "employer_homepage"),
    path("applications/<int:job_id>/", employerView.ViewApplication.as_view(), name = "view_applications"),
    path("accept-job/<int:application_id>/", employerView.AcceptApplicationView.as_view(), name = "accept_application"),
    path("reject-job/<int:application_id>/", employerView.RejectApplicationView.as_view(), name = "reject_application"),
]