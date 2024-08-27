from rest_framework  import serializers
from django.contrib.auth.models import User
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    class Meta:
        model = Patient
        fields = '__all__'
    
    def create(self, validated_data):
        # Extract the user_id from the validated data
        user = validated_data.pop('users')
        
        # Create the patient instance
        patient = Patient.objects.create(
            user=user,
            **validated_data
        )
        return patient

    def update(self, instance, validated_data):
        # Extract the user_id from the validated data
        user = validated_data.pop('users', None)
        
        # Update the instance with the validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update the user if provided
        if user is not None:
            instance.user = user
        
        # Save the updated instance
        instance.save()
        return instance

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
    
    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        
        if password != password2:
            raise serializers.ValidationError({'error' : "Password Dosen't Matched"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error' : "Email already exists !!"})
        
        account = User(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email
        )
        account.set_password(password)
        account.is_active = False
        account.save()
        
        return account
    
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    