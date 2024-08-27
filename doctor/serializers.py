from rest_framework  import serializers
from django.contrib.auth.models import User
from .models import (
    Doctor,
    Designation,
    Specialization,
    AvailableTime,
    Review
)

class DoctorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    
    designation = serializers.StringRelatedField(many=True, read_only=True)
    designations = serializers.PrimaryKeyRelatedField(queryset=Designation.objects.all(), many=True, write_only=True)

    specialization = serializers.StringRelatedField(many=True, read_only=True)
    specializations = serializers.PrimaryKeyRelatedField(queryset=Specialization.objects.all(), many=True, write_only=True)

    available_time = serializers.StringRelatedField(many=True, read_only=True)
    available_times = serializers.PrimaryKeyRelatedField(queryset=AvailableTime.objects.all(), many=True, write_only=True)
    
    class Meta:
        model = Doctor
        fields = '__all__'
    
    def create(self, validated_data):
        user = validated_data.pop('users')
        designation = validated_data.pop('designations', [])
        specialization = validated_data.pop('specializations', [])
        available_time = validated_data.pop('available_times', [])
        
        # Create the appointment with the correct foreign key relations
        doctor = Doctor.objects.create(
            user=user, 
            **validated_data
        )
        doctor.specialization.set(specialization)
        doctor.designation.set(designation)
        doctor.available_time.set(available_time)
        
        return doctor
    
    def update(self, instance, validated_data):
        # Handle many-to-many fields
        designations = validated_data.pop('designations', None)
        specializations = validated_data.pop('specializations', None)
        available_times = validated_data.pop('available_times', None)
        user = validated_data.pop('users', None)
        
        # Update fields on the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update many-to-many fields
        if designations is not None:
            instance.designation.set(designations)
        if specializations is not None:
            instance.specialization.set(specializations)
        if available_times is not None:
            instance.available_time.set(available_times)
        
        # Update the user if provided
        if user is not None:
            instance.user = user
        
        instance.save()
        return instance

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class AvailableTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableTime
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
    