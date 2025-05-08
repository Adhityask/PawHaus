from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Pet(models.Model): # type: ignore
    name=models.CharField(max_length=30)
    age=models.IntegerField()
    img=models.ImageField(upload_to='image',default='')
    type=models.CharField(max_length=20)
    breed=models.CharField(max_length=20)
    gender=models.CharField(max_length=6,default="")
    details=models.CharField(max_length=100,default='')
    price=models.IntegerField()

class Cart(models.Model):
    uid= models.ForeignKey(User,on_delete=models.CASCADE, db_column='uid')
    pid= models.ForeignKey(Pet,on_delete=models.CASCADE,db_column='petid')
    quantity = models.IntegerField(default=1)
    

class Order (models.Model):
    orderid = models.CharField(max_length=50)
    userid= models.ForeignKey(User,on_delete=models.CASCADE, db_column = 'userid')
    petid= models.ForeignKey(Pet, on_delete=models.CASCADE, db_column='petid')
    quantity = models.IntegerField()
    totallBill= models.IntegerField()