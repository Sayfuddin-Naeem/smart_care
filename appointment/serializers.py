from rest_framework  import serializers
from .models import Appointment
from patient.models import Patient
from doctor.models import Doctor, AvailableTime

class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField(many=False)
    patient_name = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), write_only=True)
    
    doctor = serializers.StringRelatedField(many=False)
    doctor_name = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), write_only=True)
    
    time = serializers.StringRelatedField(many=False)
    select_time = serializers.PrimaryKeyRelatedField(queryset=AvailableTime.objects.all(), write_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'
    
    def create(self, validated_data):
        patient = validated_data.pop('patient_name')
        doctor = validated_data.pop('doctor_name')
        time = validated_data.pop('select_time')
        
        # Create the appointment with the correct foreign key relations
        appointment = Appointment.objects.create(
            patient=patient, 
            doctor=doctor, 
            time=time, 
            **validated_data
        )
        return appointment
    
    def update(self, instance, validated_data):
        patient = validated_data.pop('patient_name', None)
        doctor = validated_data.pop('doctor_name', None)
        time = validated_data.pop('select_time', None)
        
        # Update fields on the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update relationships if provided
        if patient is not None:
            instance.patient = patient
        if doctor is not None:
            instance.doctor = doctor
        if time is not None:
            instance.time = time
        
        instance.save()
        return instance
    