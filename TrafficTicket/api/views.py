from django.shortcuts import render
from rest_framework import viewsets,permissions
from django.contrib.auth.models import  User
# Create your views here.

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
    Violation
)
from api.serializers import (ViolationTypeSerializer,UserSerializer,AdminSerializer,PersonSerializer,DriverSerializer,VehicleOwnerSerializer,VehicleSerializer,FineSerializer,AccidentSerializer,MessageSerializer,PoliceOfficerSerializer,ViolationSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


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


