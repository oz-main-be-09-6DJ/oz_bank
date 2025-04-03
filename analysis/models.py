from django.contrib.auth import get_user_model
from django.db import models
from utils.constants import ANALYSIS_TYPES,ANALYSIS_ABOUT

User = get_user_model()

class Analysis(models.Model):
    analysis_about = models.CharField(max_length=20, null=False, choices=ANALYSIS_ABOUT)
    analysis_type = models.CharField(max_length=10, null=False, choices=ANALYSIS_TYPES)
    period_start = models.DateField(null=False, blank=False)
    period_end = models.DateField(null=False, blank=False)
    analysis_description = models.CharField(max_length=100, null=False, blank=False, default="")
    result_image = models.TextField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="analysis")

    def __str__(self):
        return f"[{self.get_analysis_about_display()}] {self.analysis_description}"


