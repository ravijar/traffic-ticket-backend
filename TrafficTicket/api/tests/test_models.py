from django.test import TestCase
from api.models import Admin, Vehicle, VehicleOwner, Fine, Driver, Person, Accident, Message, PoliceOfficer, ViolationType, Violation, Suggestion
from django.contrib.auth.models import User
from datetime import date
from datetime import time

class AdminModelTest(TestCase):
    def test_admin_creation(self):
        user = User.objects.create(username="adminuser", email="admin@example.com")
        admin = Admin.objects.create(user=user, police_station="Test Police Station")
        self.assertEqual(admin.user, user)
        self.assertEqual(str(admin), admin.user.username)

class VehicleModelTest(TestCase):
    def test_vehicle_creation(self):
        vehicle = Vehicle.objects.create(
            vehicle_number="ABC123",
            chassis_number="1234567890",
            engine_number="0987654321",
            vehicle_type="Car",
            color="Red",
            license_expiry_date=date(2023, 12, 31)
        )
        self.assertEqual(str(vehicle), vehicle.vehicle_number)

class VehicleOwnerModelTest(TestCase):
    def test_vehicle_owner_creation(self):
        user = User.objects.create(username="vehicleowner", email="owner@example.com")
        person = Person.objects.create(nic="123456789012", first_name="John", last_name="Doe")
        driver = Driver.objects.create(nic=person, license_id="DL1234", user=user)
        vehicle = Vehicle.objects.create(
            vehicle_number="ABC123",
            chassis_number="1234567890",
            engine_number="0987654321",
            vehicle_type="Car",
            color="Red",
            license_expiry_date=date(2023, 12, 31)
        )
        vehicle_owner = VehicleOwner.objects.create(vehicle_number=vehicle, nic=driver)
        self.assertEqual(vehicle_owner.vehicle_number, vehicle)
        self.assertEqual(vehicle_owner.nic, driver)

class FineModelTest(TestCase):
    def test_fine_creation(self):
        user = User.objects.create(username="fineuser", email="fine@example.com")
        person = Person.objects.create(nic="123456789012", first_name="John", last_name="Doe")
        driver = Driver.objects.create(nic=person, license_id="DL1234", user=user)
        vehicle = Vehicle.objects.create(
            vehicle_number="ABC123",
            chassis_number="1234567890",
            engine_number="0987654321",
            vehicle_type="Car",
            color="Red",
            license_expiry_date=date(2023, 12, 31)
        )
        violation_type = ViolationType.objects.create(violation_type="Speeding", fine_amount=50.00)
        fine = Fine.objects.create(
            vehicle=vehicle,
            driver=driver,
            time="12:00:00",
            date=date(2023, 10, 1),
            violation=violation_type,
            location="Test Location",
            description="Test Description",
            due_date=date(2023, 11, 1),
            payment_status=False
        )
        self.assertEqual(fine.vehicle, vehicle)
        self.assertEqual(fine.driver, driver)

# Add similar test cases for other models

class DriverModelTest(TestCase):
    def test_driver_creation(self):
        user = User.objects.create(username="driveruser", email="driver@example.com")
        person = Person.objects.create(nic="123456789012", first_name="John", last_name="Doe")
        driver = Driver.objects.create(nic=person, license_id="DL1234", user=user)
        self.assertEqual(driver.nic, person)
        self.assertEqual(driver.user, user)

class PersonModelTest(TestCase):
    def test_person_creation(self):
        person = Person.objects.create(nic="123456789012", first_name="John", last_name="Doe")
        self.assertEqual(str(person), person.first_name + " " + person.last_name)

class AccidentModelTest(TestCase):
    def test_accident_creation(self):
        user = User.objects.create(username="accidentuser", email="accident@example.com")
        person = Person.objects.create(nic="123456789012", first_name="John", last_name="Doe")
        driver = Driver.objects.create(nic=person, license_id="DL1234", user=user)
        accident = Accident.objects.create(
            time=time(12, 0),
            date=date(2023, 10, 1),
            location="Test Location",
            description="Test Description",
            reporter=driver
        )
        self.assertEqual(accident.reporter, driver)

class MessageModelTest(TestCase):
    def test_message_creation(self):
        message = Message.objects.create(
            sender_nic="123456789012",
            body="Test Message"
        )
        self.assertEqual(str(message), message.body)

class PoliceOfficerModelTest(TestCase):
    def test_police_officer_creation(self):
        user = User.objects.create(username="policeuser", email="police@example.com")
        person = Person.objects.create(nic="123456789012", first_name="John", last_name="Doe")
        police_officer = PoliceOfficer.objects.create(user=user, nic=person, police_station="Test Police Station")
        self.assertEqual(police_officer.nic, person)
        self.assertEqual(police_officer.user, user)

class ViolationTypeModelTest(TestCase):
    def test_violation_type_creation(self):
        violation_type = ViolationType.objects.create(violation_type="Speeding", fine_amount=50.00)
        self.assertEqual(str(violation_type), violation_type.violation_type)

class ViolationModelTest(TestCase):
    def test_violation_creation(self):
        violation_type = ViolationType.objects.create(violation_type="Speeding", fine_amount=50.00)
        violation = Violation.objects.create(
            violation=violation_type,
            time=time(12, 0),
            date=date(2023, 10, 1),
            location="Test Location",
            original_image=b'',
            vehicle_image=b'',
            license_plate_image=b'',
            detected_license_plate="ABC1234"
        )
        self.assertEqual(violation.violation, violation_type)
        self.assertEqual(violation.detected_license_plate, "ABC1234")

class SuggestionModelTest(TestCase):
    def test_suggestion_creation(self):
        suggestion = Suggestion.objects.create(suggestion="Test Suggestion")
        self.assertEqual(str(suggestion), suggestion.suggestion)



