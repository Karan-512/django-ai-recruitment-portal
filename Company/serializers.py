from rest_framework import serializers
from .models import JobPosting, Application
from .models import JobPosting, CompanyProfile
from Authentication.serializers import UserSerializer

class CompanyProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = CompanyProfile
        fields = "__all__"


class JobPostingSerializer(serializers.ModelSerializer):
    applicant_count = serializers.IntegerField(source='application_set.count', read_only=True)
    company = CompanyProfileSerializer(read_only=True)

    class Meta:
        model = JobPosting
        fields = '__all__'


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





