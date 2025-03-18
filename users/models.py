
from django.db import models

class Register(models.Model):

    User_Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Email = models.EmailField()
    Number = models.CharField(max_length=20)
    Username = models.CharField(max_length=30)
    Password = models.CharField(max_length=255)

    class Meta:
        db_table = "Register"

class User_Details(models.Model):

     Case_Id = models.AutoField(primary_key=True)
     User = models.ForeignKey(Register, on_delete=models.CASCADE)
     Name = models.CharField(max_length=255)
     Number =  models.CharField(max_length=12)
     Email = models.EmailField()
     Address = models.TextField()
     City = models.CharField(max_length=100)
     District = models.CharField(max_length=100,default=1)
     State = models.CharField(max_length=100)

     class Meta:
         db_table = "User_Details"

class Case_Details(models.Model):

    Id = models.AutoField(primary_key=True)
    Case = models.ForeignKey(User_Details, on_delete=models.CASCADE)  # No need for default=1
    Complaint_Type = models.CharField(max_length=100)
    Complaint_Subject = models.CharField(max_length=255)
    Complaint_Area = models.CharField(max_length=100)
    Complaint_Date = models.DateField()
    Complaint_Details = models.TextField()
    Complaint_Image = models.ImageField(upload_to='media/')


    class Meta:
         db_table="Case_Details"

class Lawyer_Register(models.Model):

    Lawyer_Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Email = models.EmailField()
    Number = models.CharField(max_length=20)
    Experience = models.DecimalField(max_digits=2,decimal_places=1)
    Firm = models.CharField(max_length=255)
    Category = models.CharField(max_length=25)
    Image = models.ImageField(upload_to='media/')
    Price = models.IntegerField()

    class Meta:
        db_table = "Lawyer_Register"



class Basic_Laws(models.Model):

    Law_Id = models.AutoField(primary_key=True)
    Law_Title = models.CharField(max_length=60)
    Law_Category = models.CharField(max_length=25)
    Law_Relevant = models.CharField(max_length=255)
    Law_Punishment = models.TextField()
    Law_Description = models.TextField()
    Law_link = models.CharField(max_length=100)

    class Meta:
        db_table='Basic_Laws'


class Book_Lawyer(models.Model):

    Book_Id = models.AutoField(primary_key=True)
    User = models.ForeignKey(Register, on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)
    Number = models.CharField(max_length=255)
    Email = models.EmailField()
    City = models.CharField(max_length=100)
    District =models.CharField(max_length=100,default=1)
    State = models.CharField(max_length=100)

    Lawyer_Name = models.CharField(max_length=255)
    Category = models.CharField(max_length=25)
    Appointment_Date = models.DateField()
    Appointment_Time = models.CharField(max_length=100)
    Contact_Time = models.CharField(max_length=100)

    class Meta:
        db_table = 'Book_Lawyer'

class Payment_Details(models.Model):

    Pay_Id = models.AutoField(primary_key=True)
    Book = models.ForeignKey(Book_Lawyer, on_delete=models.CASCADE)
    User = models.ForeignKey(Register, on_delete=models.CASCADE)
    CardName = models.CharField(max_length=100)
    CardNumber = models.CharField(max_length=30)
    CardExpiryMonth = models.CharField(max_length=10)
    CardExpiryYear = models.CharField(max_length=4)
    Cvv = models.CharField(max_length=4)
    Price = models.IntegerField()

    class Meta:
        db_table='Payment_Details'

class Emergency_Numbers(models.Model):

    Num_Id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=100)
    Number = models.CharField(max_length=100)

    class Meta:
        db_table='Emergency_Numbers'




# Create your models here.
