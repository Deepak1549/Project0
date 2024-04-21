from django.db import models
from .userModel import UserModel

EXPERIENCE_OPTIONS = [
    (1, "0-1 year"),
    (2, "1-2 years"),
    (3, "2-3 years"),
    (4, "3-4 years"),
    (5, "4-5 years"),
    (0, "Any"),
]

class JobModel(models.Model):
    employer = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.TextField()
    experience = models.IntegerField(choices=EXPERIENCE_OPTIONS, null=True, blank=True)
    contact_us = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @property
    def applicants(self):
        from api.models.applyJobModel import ApplyJobModel
        applications = ApplyJobModel.objects.filter(job = self.id).count()
        return applications


    class Meta:
        db_table = "Jobs"
        ordering = ["-created_at"]