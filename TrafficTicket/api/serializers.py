from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import (
    Admin,
    Person,
    Driver, 
    VehicleOwner,
    Vehicle,
    Fine,
    ViolationType,
    Accident,
    Message,
    PoliceOfficer,
    Violation,
    Suggestion,
    Schedule,
    VehicleAccident,
    OTPVerification
)

# Generic Serializers ------------------------------------------------------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class VehicleOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleOwner
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = '__all__'



class ViolationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViolationType
        fields = '__all__'


class FineIdSerializer(serializers.ModelSerializer):
    violation_type = serializers.CharField(source='violation.violation_type')

    class Meta:
        model = Fine
        fields = ('fine_id', 'date', 'violation_type', 'location', 'payment_status')


class AccidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accident
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class PoliceOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceOfficer
        fields = '__all__'


class ViolationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Violation
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = '__all__'

class VehicleAccidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleAccident
        fields = '__all__'

# Custom Serializers ------------------------------------------------------------------

class FineWithViolationAmountSerializer(serializers.ModelSerializer):
    # Create a read-only field to get the amount from ViolationType
    violation_amount = serializers.DecimalField(max_digits=10, decimal_places=2, source='violation.fine_amount', read_only=True)
    fine_id = serializers.IntegerField(label='ID')
    class Meta:
        model = Fine
        # Specify the fields you want to include in the response
        fields = ('fine_id', 'vehicle', 'date', 'time', 'violation_amount')


class scheduledOfficersSerializer(serializers.ModelSerializer):
    officer_id = serializers.CharField(source='officer.officer_id')
    telephone = serializers.CharField(source='officer.nic.telephone')
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f"{obj.officer.nic.first_name} {obj.officer.nic.last_name}"

    class Meta:
        model = Schedule
        fields = ['location','shift','officer_id','full_name','telephone']
        
class DriverDetailsSerializer(serializers.ModelSerializer):
    nic = serializers.CharField(source='nic.nic.nic')
    full_name = serializers.SerializerMethodField()
    telephone = serializers.CharField(source='nic.nic.telephone')
    vehicle_number = serializers.CharField(source='vehicle_number.vehicle_number')

    def get_full_name(self, obj):
        return f"{obj.nic.nic.first_name} {obj.nic.nic.last_name}"
    
    class Meta:
        model = VehicleOwner
        fields = ['nic','full_name','vehicle_number','telephone']

class OfficerDetailsSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    telephone = serializers.CharField(source='nic.telephone')

    def get_full_name(self, obj):
        return f"{obj.nic.first_name} {obj.nic.last_name}"

    class Meta:
        model = PoliceOfficer
        fields = ['officer_id','full_name','nic','police_station','telephone']

class FineDetailsSerializer(serializers.ModelSerializer):
    driver_nic = serializers.CharField(source='driver.nic.nic')
    vehicle_number = serializers.CharField(source='vehicle.vehicle_number')
    violation_type = serializers.CharField(source='violation.violation_type')
    payment = serializers.SerializerMethodField()

    def get_payment(self, obj):
        if obj.payment_status:
            return "Paid"
        else:
            return "Not Paid"

    class Meta:
        model = Fine
        fields = ['fine_id','driver_nic','vehicle_number','location','date','time','violation_type','due_date','payment']

class AccidentDetailsSerializer(serializers.ModelSerializer):
    vehicles = serializers.SerializerMethodField()

    def get_vehicles(self, instance):
        # Get the related vehicles for the given accident instance
        vehicle_accidents = VehicleAccident.objects.filter(accident=instance)
        vehicles = '\n'.join([va.vehicle.vehicle_number for va in vehicle_accidents])
        return vehicles

    class Meta:
        model = Accident
        fields = ['location','date','time','description','vehicles']

class OTPVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPVerification
        fields = '__all__'