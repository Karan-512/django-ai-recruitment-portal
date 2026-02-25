from rest_framework import serializers
from .models import JobPosting, Application


class JobPostingSerializer(serializers.ModelSerializer):
    applicant_count = serializers.IntegerField(source='application_set.count', read_only=True)

    class Meta:
        model = JobPosting
        fields = [
            'id',
            'job_title',
            'location',
            'posted_date',
            'deadline',
            'is_closed',
            'applicant_count'
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='applicant.user.username')

    class Meta:
        model = Application
        fields = [
            'id',
            'applicant_name',
            'resume',
            'applied_date'
        ]