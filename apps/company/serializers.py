from rest_framework import serializers
from .models import Company, Country, Department, Municipality

class CompanySerializer(serializers.ModelSerializer):
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    municipality = serializers.PrimaryKeyRelatedField(queryset=Municipality.objects.all())

    class Meta:
        model = Company
        fields = [
            'id', 'nit', 'name', 'address', 'phone',
            'country', 'department', 'municipality',
            'is_active', 'deleted_at', 'created_at'
        ]
        read_only_fields = ['is_active', 'deleted_at', 'created_at']

    def validate(self, data):
        country = data.get('country')
        department = data.get('department')
        municipality = data.get('municipality')

        if department.country != country:
            raise serializers.ValidationError({
                "department": "Selected department does not belong to the selected country."
            })

        if municipality.department != department:
            raise serializers.ValidationError({
                "municipality": "Selected municipality does not belong to the selected department."
            })

        return data

class CompanyReadSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    municipality = serializers.StringRelatedField()

    class Meta:
        model = Company
        fields = [
            'id', 'nit', 'name', 'address', 'phone',
            'country', 'department', 'municipality',
            'is_active', 'deleted_at', 'created_at'
        ]

class CompanyPublicSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    municipality = serializers.StringRelatedField()

    class Meta:
        model = Company
        fields = [
            'id', 'name', 'address', 'phone',
            'country', 'department', 'municipality',
            'created_at'
        ]