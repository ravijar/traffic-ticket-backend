from django.test import SimpleTestCase
from django.urls import reverse,resolve
from api.views import (UserViewSet,
                       ViolationTypeViewSet,
                       AdminViewSet,
                       PersonViewSet,
                       DriverViewSet,
                       VehicleOwnerViewSet,
                       VehicleViewSet,
                       AccidentViewSet,
                       MessageViewSet,
                       PoliceOfficerViewSet,
                       ViolationViewSet,
                       SuggestionViewSet,
                       FineViewSet,
                       FineList,
                       MyTokenObtainPairView,
)
from rest_framework_simplejwt.views import TokenRefreshView

class TestUrls(SimpleTestCase):

    def test_userviewlist_resolves(self):
        url = reverse('user-list')
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, UserViewSet)

    def test_violationtypelist_resolves(self):
        url = reverse('violationtype-list')
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, ViolationTypeViewSet)

    def test_adminlist_resolves(self):
        url = reverse('admin-list')
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, AdminViewSet)

    def test_personlist_resolves(self):
        url = reverse('person-list')
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, PersonViewSet)

    def test_driverlist_resolves(self):
        url = reverse('driver-list')
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, DriverViewSet)

    def test_vehicleownerlist_resolves(self):
        url = reverse('vehicleowner-list')
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, VehicleOwnerViewSet)
    
    def test_vehiclelist_resolves(self):
        url = reverse('vehicle-list')
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, VehicleViewSet)

    def test_accidentlist_resolves(self):
        url = reverse('accident-list')
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, AccidentViewSet)

    def test_messagelist_resolves(self):
        url = reverse('message-list')
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, MessageViewSet)

    def test_policeofficerlist_resolves(self):
        url = reverse('policeofficer-list')
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, PoliceOfficerViewSet)

    def test_violationlist_resolves(self):
        url = reverse('violation-list')
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, ViolationViewSet)

    def test_suggestionlist_resolves(self):
        url = reverse('suggestion-list')
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, SuggestionViewSet)

    def test_finelist_resolves(self):
        url = reverse('fine-list')
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, FineList)

    def test_filtered_fine_list_url_resolves(self):
        url = reverse('filtered-fine-list', args=['your_driver_id_here'])
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, FineList)

    def test_rest_auth_url_resolves(self):
        url = reverse('rest_framework:login')
        resolved = resolve(url)
        self.assertEqual(resolved.func.__name__, 'LoginView')

    def test_token_obtain_url_resolves(self):
        url = reverse('token_obtain_pair')
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, MyTokenObtainPairView)

    def test_token_refresh_url_resolves(self):
        url = reverse('token_refresh')
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, TokenRefreshView)