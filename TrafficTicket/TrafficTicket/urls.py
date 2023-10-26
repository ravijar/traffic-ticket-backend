"""TrafficTicket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from api import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"violationtypes", views.ViolationTypeViewSet)  
router.register(r"admins", views.AdminViewSet)
router.register(r"persons", views.PersonViewSet)
router.register(r"drivers", views.DriverViewSet)
router.register(r"vehicleowners", views.VehicleOwnerViewSet)
router.register(r"vehicles", views.VehicleViewSet)
router.register(r"fines", views.FineViewSet)
router.register(r"accidents", views.AccidentViewSet)
router.register(r"messages", views.MessageViewSet)
router.register(r"policeofficers", views.PoliceOfficerViewSet)
router.register(r"violations", views.ViolationViewSet)
router.register(r"suggestions", views.SuggestionViewSet)
router.register(r"schedules", views.ScheduleViewSet)
router.register(r"fines", views.FineViewSet)
router.register(r"vehicleaccidents", views.VehicleAccidentViewSet)
router.register(r"otpverifications", views.OTPVerificationViewSet)
router.register(r"officerlocations", views.OfficerLocationViewSet)
router.register(r"camerlocations", views.CameraLocationViewSet)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(router.urls)),
    path('api/driverfine/', views.FineList.as_view(), name='fine-list'),
    path('api/driverfine/<str:driver_id>/', views.FineList.as_view(), name='filtered-fine-list'),
    path("api/rest-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/send_otp/', views.UserViewSet.as_view({'post': 'send_otp'}), name='send-otp'),
    path('api/verify_otp/', views.UserViewSet.as_view({'post': 'verify_otp'}), name='verify-otp'),
    path('api/finebyid/<str:driver_id>/', views.FineByIdViewSet.as_view({'get':'list'}), name='fine-by-driver'),
    

]
