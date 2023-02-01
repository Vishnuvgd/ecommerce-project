from django.db import models

# Create your models here.

class regmodel(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class shopregmodel(models.Model):
    sname=models.CharField(max_length=20)
    semail=models.EmailField()
    spassword=models.CharField(max_length=25)

    def __str__(self):
        return self.sname

class uploadmodel(models.Model):
    name=models.CharField(max_length=25)
    image=models.ImageField(upload_to="eapp/static")
    price=models.IntegerField()
    description=models.CharField(max_length=30)

    def __str__(self):
        return self.name

class addcartmodel(models.Model):
    cartname = models.CharField(max_length=25)
    cartimage = models.ImageField(upload_to="eapp/static")
    cartprice = models.IntegerField()
    cartdescription = models.CharField(max_length=30)

    def __str__(self):
        return self.cartname