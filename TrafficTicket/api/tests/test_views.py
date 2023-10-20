from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

class TestViews(TestCase):

    def test_user_create_view(self):
        url = reverse('user-list')
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_violation_type_list_view(self):
        url = reverse('violationtype-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_list_view(self):
        url = reverse('admin-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_person_list_view(self):
        url = reverse('person-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_driver_list_view(self):
        url = reverse('driver-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vehicle_owner_list_view(self):
        url = reverse('vehicleowner-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vehicle_list_view(self):
        url = reverse('vehicle-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accident_list_view(self):
        url = reverse('accident-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_message_list_view(self):
        url = reverse('message-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_police_officer_list_view(self):
        url = reverse('policeofficer-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_violation_list_view(self):
        url = reverse('violation-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_suggestion_list_view(self):
        url = reverse('suggestion-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fine_list_view(self):
        url = reverse('fine-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filtered_fine_list_view(self):
        
        driver_id = '200023003421'
        url = reverse('filtered-fine-list', args=[driver_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
