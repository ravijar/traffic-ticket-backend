from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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
    OfficerLocation,
    CameraLocation,
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


class OfficerLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficerLocation
        fields = '__all__'


class CameraLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraLocation
        fields = '__all__'


class OTPVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPVerification
        fields = '__all__'

# Custom Serializers ------------------------------------------------------------------


# driver mobile fines
class FineWithViolationAmountSerializer(serializers.ModelSerializer):
    violation_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, source='violation.fine_amount', read_only=True)
    fine_id = serializers.IntegerField(label='ID')

    class Meta:
        model = Fine
        fields = ('fine_id', 'vehicle', 'date', 'time', 'violation_amount')


# admin web schedules
class scheduledOfficersSerializer(serializers.ModelSerializer):
    officer_id = serializers.CharField(source='officer.officer_id')
    telephone = serializers.CharField(source='officer.nic.telephone')
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f"{obj.officer.nic.first_name} {obj.officer.nic.last_name}"

    class Meta:
        model = Schedule
        fields = ['location', 'shift', 'officer_id', 'full_name', 'telephone']


# admin web driver details
class DriverDetailsSerializer(serializers.ModelSerializer):
    nic = serializers.CharField(source='nic.nic')
    full_name = serializers.SerializerMethodField()
    email = serializers.CharField(source='user.email')
    vehicle_number = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f"{obj.nic.first_name} {obj.nic.last_name}"

    def get_vehicle_number(self, instance):
        vehicle_owners = VehicleOwner.objects.filter(nic=instance)
        vehicles = '\n'.join(
            [va.vehicle_number.vehicle_number for va in vehicle_owners])
        return vehicles

    class Meta:
        model = Driver
        fields = ['nic', 'full_name', 'vehicle_number', 'email']


# admin web police officer details
class OfficerDetailsSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    telephone = serializers.CharField(source='nic.telephone')

    def get_full_name(self, obj):
        return f"{obj.nic.first_name} {obj.nic.last_name}"

    class Meta:
        model = PoliceOfficer
        fields = ['officer_id', 'full_name',
                  'nic', 'police_station', 'telephone']


# admin web fine details
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
        fields = ['fine_id', 'driver_nic', 'vehicle_number', 'location',
                  'date', 'time', 'violation_type', 'due_date', 'payment']


# admin web accident details
class AccidentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accident
        fields = ['location', 'date', 'time', 'description', 'reporter']


# admin web recent accidents
class RecentAccidentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accident
        fields = ['index', 'location', 'date', 'time']


# admin web police station locations
class PoliceStationLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficerLocation
        fields = ['location']


# admin web vehicle details
class VehicleDetailsSerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField()

    def get_owner_name(self, instance):
        # Get the related vehicles for the given accident instance
        vehicle_owners = VehicleOwner.objects.filter(vehicle_number=instance)
        owner = '\n'.join([va.nic.nic.first_name for va in vehicle_owners])
        return owner

    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'chassis_number', 'engine_number',
                  'vehicle_type', 'color', 'license_expiry_date', 'owner_name']


# officer mobile fines
class FineIdSerializer(serializers.ModelSerializer):
    violation_type = serializers.CharField(source='violation.violation_type')

    class Meta:
        model = Fine
        fields = ('fine_id', 'date', 'violation_type',
                  'location', 'payment_status')


# custom token serializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print("get token", user.username)
        token = super().get_token(user)
        print(token.__str__())
        # custom fields
        token['username'] = user.username
        token['role'] = user.groups.all()[0].name
        # taking the police station of the admins
        if (user.groups.all()[0].name == "admin"):
            police_station = Admin.objects.get(user=user).police_station
            token['police_station'] = police_station

        return token