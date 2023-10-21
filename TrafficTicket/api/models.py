from django.db import models
from django.contrib.auth.models import User

#done
class Admin(models.Model):
    # user_id = models.CharField(max_length=12, primary_key=True)
    # password = models.CharField(max_length=128)  
    police_station = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

#done
class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=7, primary_key=True)
    owner_name = models.CharField(max_length=100, default="Unknown")
    chassis_number = models.CharField(max_length=20)
    engine_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=20)
    color = models.CharField(max_length=10)
    license_expiry_date = models.DateField()

#done
class VehicleOwner(models.Model):
    vehicle_number = models.OneToOneField('Vehicle', primary_key=True, on_delete=models.CASCADE)
    nic = models.ForeignKey('Driver', on_delete=models.CASCADE)

#done
class Fine(models.Model):
    fine_id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    time = models.TimeField()
    date = models.DateField()
    violation = models.ForeignKey('ViolationType', on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    due_date = models.DateField()
    payment_status = models.BooleanField()

#driver
class Driver(models.Model):
    nic = models.OneToOneField('Person', primary_key=True, on_delete=models.CASCADE)
    # password = models.CharField(max_length=128)  
    license_id = models.CharField(max_length=8)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

#done
class Person(models.Model):
    nic = models.CharField(max_length=12, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    telephone = models.CharField(max_length=10)
    address = models.CharField(max_length=200)

#done
class Accident(models.Model):
    index = models.AutoField(primary_key=True)
    time = models.TimeField()
    date = models.DateField()
    location = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    reporter = models.ForeignKey('Driver', on_delete=models.CASCADE)



class Message(models.Model):
    index = models.AutoField(primary_key=True)
    sender_nic = models.CharField(max_length=12)
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=1000)



#done
class PoliceOfficer(models.Model):
    nic = models.OneToOneField('Person', primary_key=True, on_delete=models.CASCADE)
    # password = models.CharField(max_length=128)  
    police_station = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


#done
class ViolationType(models.Model):
    violation_id = models.AutoField(primary_key=True)
    violation_type = models.CharField(max_length=50)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2)



# done
class Violation(models.Model):
    index = models.AutoField(primary_key=True)
    violation = models.ForeignKey('ViolationType', on_delete=models.CASCADE)
    time = models.TimeField()
    date = models.DateField()
    location = models.CharField(max_length=50)
    original_image = models.BinaryField()
    vehicle_image = models.BinaryField()
    license_plate_image = models.BinaryField()
    detected_license_plate = models.CharField(max_length=7)

