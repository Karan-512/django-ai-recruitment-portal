
from rest_framework import serializers
from .models import JobPosting, CompanyProfile


class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = "__all__"


class JobPostingSerializer(serializers.ModelSerializer):
    company = CompanyProfileSerializer(read_only=True)
    class Meta:
        model = JobPosting
        fields = '__all__'