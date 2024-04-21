from django.db import models
from api.models.userModel import UserModel
from api.models.jobModel import JobModel

STATUS_CHOICES = [
    (1, "APPLIED"),
    (2, "ACCEPTED"),
    (3, "REJECTED"),
]

class ApplyJobModel(models.Model):
    employee = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    job = models.ForeignKey(JobModel, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(upload_to="resumes")

    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "Employee Jobs"