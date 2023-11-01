from django.shortcuts import render
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User, Group
from rest_framework_simplejwt.views import TokenObtainPairView
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
    OTPVerification,
    CameraLocation,
    OfficerLocation
)
from api.serializers import (
    ViolationTypeSerializer,
    UserSerializer,
    AdminSerializer,
    PersonSerializer,
    DriverSerializer,
    VehicleOwnerSerializer,
    VehicleSerializer,
    FineSerializer,
    AccidentSerializer,
    MessageSerializer,
    PoliceOfficerSerializer,
    ViolationSerializer,
    FineWithViolationAmountSerializer,
    SuggestionSerializer,
    ScheduleSerializer,
    scheduledOfficersSerializer,
    DriverDetailsSerializer,
    OfficerDetailsSerializer,
    FineDetailsSerializer,
    AccidentDetailsSerializer,
    VehicleAccidentSerializer,
    OTPVerificationSerializer,
    RecentAccidentsSerializer,
    OfficerLocationSerializer,
    CameraLocationSerializer,
    PoliceStationLocationsSerializer,
    FineIdSerializer,
    VehicleDetailsSerializer,
    MyTokenObtainPairSerializer
)

from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.core.mail import send_mail
from pyotp import TOTP
import random
import string
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.functions import ExtractMonth, ExtractDay
from datetime import date, timedelta


# jwt token view
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    # driver mobile driver signup
    @action(detail=False, methods=["post"])
    def driver_signup(self, request):
        """Register a new user.
            api [POST] /api/users/driver_signup/]
            required ['password', 'email', 'first_name', 'last_name', 'nic', 'license_id']]"""

        user = User.objects.create_user(
            username=request.data["nic"],
            password=request.data["password"],
            email=request.data["email"],
        )
        group = Group.objects.get(name="driver")
        user.groups.add(group)
        user.save()
        p, is_created = Person.objects.get_or_create(
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            defaults={"nic": request.data["nic"]},
        )
        driver = Driver.objects.create(
            nic=p,
            license_id=request.data["license_id"],
            user=user,
        )
        driver.save()
        return Response({"status": "driver created"}, status=status.HTTP_201_CREATED)

    # driver/officer mobile change password
    @action(detail=False, methods=["put"])
    def change_password(self, request):
        """
        Change a user's password.
        api [POST] /api/users/change_password/
        required: ['nic', 'old_password', 'new_password']
        """
        nic = request.data.get("nic")
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not nic or not old_password or not new_password:
            return Response(
                {"error": "NIC, old password, and new password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(username=nic)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            # Update the session to avoid having to re-login

            return Response({"status": "password changed"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # admin web officer signup
    @action(detail=False, methods=["post"])
    def officer_signup(self, request):
        """Register a new user.
            api [POST] /api/users/officer_signup/]
            required ['password', 'first_name', 'last_name', 'telephone','nic', 'police_station']]"""
        print("officer signup")
        print(request.data)
        user = User.objects.create_user(
            username=request.data["officer_id"],
            password=request.data["password"],
        )
        group = Group.objects.get(name="officer")
        user.groups.add(group)
        user.save()
        p, is_created = Person.objects.get_or_create(
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            telephone=request.data["telephone"],
            address="",
            defaults={"nic": request.data["nic"]},
        )
        officer = PoliceOfficer.objects.create(
            nic=p,
            police_station=request.data["police_station"],
            officer_id=request.data["officer_id"],
            user=user,
        )
        officer.save()
        return Response({"status": "officer created"}, status=status.HTTP_201_CREATED)

    # driver/officer mobile send otp
    @action(detail=False, methods=["post"])
    def send_otp(self, request):
        """
        Generate and send an OTP to the user's email.
        api [POST] /api/users/send_otp/
        required: ['nic']
        """
        nic = request.data.get("nic")

        try:
            user = User.objects.get(username=nic)

        except User.DoesNotExist:
            return Response({"error": "User not found."},  status=status.HTTP_404_NOT_FOUND)

        # Check if an OTPVerification entry with the same `nic` already exists
        otp_verification, created = OTPVerification.objects.get_or_create(
            nic=nic)
        otp = ''.join(random.choices(string.digits, k=6))

        otp_verification.otp = otp
        otp_verification.save()

        totp = TOTP(otp)
        otp_url = totp.provisioning_uri(user.email, issuer_name="YourApp")

        subject = "OTP Verification"
        message = f"Your OTP for verification is: {otp}"
        from_email = "trafficticketse18@gmail.com"  # Update with your email
        recipient_list = [user.email]

        send_mail(subject, message, from_email,
                  recipient_list, fail_silently=False)

        return Response({"status": "OTP sent successfully."}, status=status.HTTP_200_OK)

    # driver/officer mobile verify otp
    @action(detail=False, methods=["post"])
    def verify_otp(self, request):
        """
        Verify the entered OTP.
        api [POST] /api/users/verify_otp/
        required: ['nic', 'entered_otp']
        """
        nic = request.data.get("nic")
        entered_otp = request.data.get("entered_otp")

        try:
            user = User.objects.get(username=nic)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            otp_verification = OTPVerification.objects.get(nic=nic)
        except OTPVerification.DoesNotExist:
            return Response({"error": "OTP not found for the user."}, status=status.HTTP_400_BAD_REQUEST)

        stored_otp = otp_verification.otp

        if (stored_otp == entered_otp):
            return Response({"status": "OTP is valid."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["put"])
    def update_password(self, request):
        """
        Change a user's password.
        api [POST] /api/users/update_password/
        required: ['nic','new_password']
        """
        nic = request.data.get("nic")
        new_password = request.data.get("new_password")

        if not nic or not new_password:
            return Response(
                {"error": "NIC and new password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(username=nic)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user.set_password(new_password)
        user.save()
        # Update the session to avoid having to re-login

        return Response({"status": "password changed"}, status=status.HTTP_200_OK)


class ViolationTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows violation types to be viewed or edited.
    """

    queryset = ViolationType.objects.all()
    serializer_class = ViolationTypeSerializer
    permission_classes = [permissions.AllowAny]


class AdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admins to be viewed or edited.
    """

    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [permissions.AllowAny]


class PersonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows persons to be viewed or edited.
    """

    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [permissions.AllowAny]


class DriverViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows drivers to be viewed or edited.
    """

    queryset = Driver.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "list":
            return DriverDetailsSerializer
        return DriverSerializer


class VehicleOwnerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows vehicle owners to be viewed or edited.
    """

    queryset = VehicleOwner.objects.all()
    serializer_class = VehicleOwnerSerializer
    permission_classes = [permissions.AllowAny]


class VehicleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows vehicles to be viewed or edited.
    """

    queryset = Vehicle.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return VehicleDetailsSerializer
        return VehicleSerializer


class FineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows fines to be viewed or edited.
    """

    queryset = Fine.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "list":
            return FineDetailsSerializer
        return FineSerializer


class FineByIdViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows a fine to be viewed or edited.
    """

    serializer_class = FineIdSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        driver_id = self.kwargs['driver_id']
        driver = Driver.objects.get(nic=driver_id)
        queryset = Fine.objects.filter(driver=driver)
        return queryset


class AccidentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accidents to be viewed or edited.
    """

    queryset = Accident.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "list":
            return AccidentDetailsSerializer
        return AccidentSerializer

    # admin web recent accidents
    @action(detail=False, methods=["GET"])
    def get_recent_accidents(self, request, *args, **kwargs):
        queryset = Accident.objects.all().order_by('-index')[:6]
        serializer = RecentAccidentsSerializer(queryset, many=True)
        return Response(serializer.data)

    # admin web monthly accident count
    @action(detail=False, methods=["GET"])
    def get_monthly_count(self, request, *args, **kwargs):
        current_year = date.today().year
        queryset = Accident.objects.filter(date__year=current_year).annotate(month=ExtractMonth(
            'date')).values('month').annotate(count=Count('index')).values('month', 'count')
        monthly_count = [0]*12
        for data in queryset:
            monthly_count[data['month']-1] = data['count']
        print(queryset)
        return Response(monthly_count)

    # admin web weekly accident count
    @action(detail=False, methods=["GET"])
    def get_weekly_count(self, request, *args, **kwargs):
        today = date.today()
        weekday = today.weekday()
        start_of_week = today - timedelta(days=weekday)
        end_of_week = start_of_week + timedelta(days=6)
        queryset = Accident.objects.filter(date__range=[start_of_week, end_of_week]).annotate(
            day=ExtractDay('date')).values('day').annotate(count=Count('index')).values('day', 'count')
        weekly_count = [0]*7
        for data in queryset:
            weekly_count[data['day']-start_of_week.day] = data['count']
        return Response(weekly_count)

    # admin web reported accident count
    @action(detail=False, methods=["GET"])
    def get_reported_accident_count(self, request, *args, **kwargs):
        today = date.today()
        queryset = Accident.objects.filter(date=today)
        return Response(queryset.count())


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # Create a list to hold the serialized data for each message
        data = []

        for message in queryset:
            # Get the sender's police officer information based on sender_nic
            try:
                sender_id = message.sender_nic
                police_officer = PoliceOfficer.objects.get(
                    officer_id=sender_id)

                police_station = police_officer.police_station
            except PoliceOfficer.DoesNotExist:
                sender_id = None
                police_station = None

            # Create a dictionary for the current message
            message_data = {
                'message_body': message.body,
                'sender_id': sender_id,
                'police_station': police_station,
            }

            data.append(message_data)

        return Response(data, status=status.HTTP_200_OK)


class PoliceOfficerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows officers to be viewed or edited.
    """

    queryset = PoliceOfficer.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "list":
            return OfficerDetailsSerializer
        return PoliceOfficerSerializer


class ViolationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows violations to be viewed or edited.
    """

    queryset = Violation.objects.all()
    serializer_class = ViolationSerializer
    permission_classes = [permissions.AllowAny]

# new


class SuggestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows suggestions to be viewed or edited.
    """

    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer
    permission_classes = [permissions.AllowAny]


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows schedules to be viewed or edited.
    """

    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.AllowAny]

    # admin web create schedule
    @action(detail=False, methods=["post"])
    def create_schedule(self, request):
        """Create a new schedule.
            api [POST] /api/schedules/create_schedule/]
            required ['officer_id', 'location', 'shift', 'date']]"""
        print("create schedule")
        print(request.data["date"])

        try:
            officer = PoliceOfficer.objects.get(
                officer_id=request.data["officer_id"])
        except:
            return Response(
                {"error": "Officer not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        schedule = Schedule.objects.create(
            officer=officer,
            location=request.data["location"],
            shift=request.data["shift"],
            date=request.data["date"],
            police_station=request.data["police_station"],
        )
        schedule.save()
        return Response({"status": "schedule created"}, status=status.HTTP_201_CREATED)

    # admin web get scheduled officers
    @action(detail=False, methods=["GET"])
    def get_scheduled_officers(self, request, *args, **kwargs):
        date = request.GET.get('date')
        policeStation = request.GET.get('police_station')
        queryset = Schedule.objects.filter(
            date=date, police_station=policeStation)
        serializer = scheduledOfficersSerializer(queryset, many=True)
        return Response(serializer.data)


class VehicleAccidentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows vehicle accidents to be viewed or edited.
    """

    queryset = VehicleAccident.objects.all()
    serializer_class = VehicleAccidentSerializer
    permission_classes = [permissions.AllowAny]


class OfficerLocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows officer locations to be viewed or edited.
    """

    queryset = OfficerLocation.objects.all()
    serializer_class = OfficerLocationSerializer
    permission_classes = [permissions.AllowAny]

    # admin web get locations related to police station
    @action(detail=False, methods=["GET"])
    def get_police_station_locations(self, request, *args, **kwargs):
        police_station = request.GET.get('police_station')
        queryset = OfficerLocation.objects.filter(
            police_station=police_station)
        serializer = PoliceStationLocationsSerializer(queryset, many=True)
        return Response(serializer.data)


class CameraLocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows camera locations to be viewed or edited.
    """

    queryset = CameraLocation.objects.all()
    serializer_class = CameraLocationSerializer
    permission_classes = [permissions.AllowAny]


class OTPVerificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = OTPVerification.objects.all()
    serializer_class = OTPVerificationSerializer
    permission_classes = [permissions.AllowAny]


class FineList(generics.ListAPIView):
    queryset = Fine.objects.all()
    serializer_class = FineWithViolationAmountSerializer

    def get_queryset(self):
        # Get the driver_id from the request query parameters
        driver_id = self.request.query_params.get('driver_id')

        # Check if driver_id is provided in the request
        if driver_id:
            # Filter the fines based on the provided driver_id
            queryset = Fine.objects.filter(driver__nic__nic=driver_id)
        else:
            # If driver_id is not provided, return an empty queryset
            queryset = Fine.objects.none()

        return queryset