from django.shortcuts import render
from rest_framework import viewsets,permissions
from django.contrib.auth.models import  User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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
    Suggestion
)
from api.serializers import (ViolationTypeSerializer,UserSerializer,AdminSerializer,PersonSerializer,DriverSerializer,VehicleOwnerSerializer,VehicleSerializer,FineSerializer,AccidentSerializer,MessageSerializer,PoliceOfficerSerializer,ViolationSerializer,FineWithViolationAmountSerializer,SuggestionSerializer)
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print("get token", user.username)
        token = super().get_token(user)
        print(token.__str__())
        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"])
    def driver_signup(self, request):
        """Register a new user.
            api [POST] /api/users/driver_signup/]
            required ['password', 'email', 'first_name', 'last_name', 'nic', 'license_id']]"""
        print("driver signup")
        print(request.data)
        user = User.objects.create_user(
            username=request.data["nic"],
            password=request.data["password"],
            email=request.data["email"],
        )
        user.save()
        p, is_created = Person.objects.get_or_create(
                first_name=request.data["first_name"],
                last_name=request.data["last_name"],
                # telephone=request.data["telephone"],
                # address=request.data["address"],
                defaults={"nic": request.data["nic"]},
            )
        driver = Driver.objects.create(
            nic=p,
            license_id=request.data["license_id"],
            user=user,
        )
        driver.save()
        return Response({"status": "driver created"}, status=status.HTTP_201_CREATED)


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
        
    @action(detail=False, methods=["post"])
    def officer_signup(self, request):
        """Register a new user.
            api [POST] /api/users/officer_signup/]
            required ['password', 'first_name', 'last_name', 'telephone','nic', 'police_station']]"""
        print("officer signup")
        print(request.data)
        user = User.objects.create_user(
            username=request.data["nic"],
            password=request.data["password"],
        )
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


class ViolationTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = ViolationType.objects.all()
    serializer_class = ViolationTypeSerializer
    permission_classes = [permissions.AllowAny]


class AdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [permissions.AllowAny]


class PersonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [permissions.AllowAny]


class DriverViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.AllowAny]


class VehicleOwnerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = VehicleOwner.objects.all()
    serializer_class = VehicleOwnerSerializer
    permission_classes = [permissions.AllowAny]


class VehicleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.AllowAny]


class FineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Fine.objects.all()
    serializer_class = FineSerializer
    permission_classes = [permissions.AllowAny]


class AccidentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Accident.objects.all()
    serializer_class = AccidentSerializer
    permission_classes = [permissions.AllowAny]


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]


class PoliceOfficerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = PoliceOfficer.objects.all()
    serializer_class = PoliceOfficerSerializer
    permission_classes = [permissions.AllowAny]


class ViolationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Violation.objects.all()
    serializer_class = ViolationSerializer
    permission_classes = [permissions.AllowAny]

# new

class SuggestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer
    permission_classes = [permissions.AllowAny]

class FineList(generics.ListAPIView):
    queryset = Fine.objects.all()
    serializer_class = FineWithViolationAmountSerializer

    # @action(detail=False, methods=["get"])
    # def get_queryset(self):     
    #     queryset = Fine.objects.all()
    #     driver_id = self.request.query_params.get('driver_id', None)
    #     if driver_id is not None:
    #         queryset = queryset.filter(driver=driver_id)
    #     return queryset

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