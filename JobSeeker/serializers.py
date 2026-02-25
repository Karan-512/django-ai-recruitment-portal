from Company.models import Application
from rest_framework import serializers

class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job_posting.job_title")
    job_id = serializers.CharField(source="job_posting.id")
    company_name = serializers.CharField(source="job_posting.company.company_name")
    location = serializers.CharField(source="job_posting.location")

    class Meta:
        model = Application
        fields = [
            "id",
            "job_title",
            "job_id",
            "company_name",
            "location",
            "application_status",
            "applied_date",
        ]