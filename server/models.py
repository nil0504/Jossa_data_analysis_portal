from django.db import models

class user_registration(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_email = models.CharField(max_length=50)
    user_password = models.CharField(max_length=16)

class main_data(models.Model):
    Institute=models.CharField(max_length=400)
    Academic_Program_Name=models.CharField(max_length=300)
    Seat_Type=models.CharField(max_length=30)
    Gender=models.CharField(max_length=30)
    Opening_Rank=models.IntegerField() 
    Closing_Rank=models.IntegerField()
    Year=models.IntegerField() 
    Round=models.IntegerField() 

