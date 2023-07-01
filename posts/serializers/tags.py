from rest_framework import serializers
from companies.models import Company


class CompanyTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name", "logo")
