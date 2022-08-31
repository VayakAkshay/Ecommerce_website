from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50,default="")
    sub_category = models.CharField(max_length=50,default="")
    product_detail = models.CharField(max_length=300)
    pub_date = models.DateField()
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='card/images',default="")

    def __str__(self):
        return self.product_name + " " + self.category

class Contact(models.Model):
    contact_id = models.AutoField(primary_key='true')
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    number = models.IntegerField(default=0)
    message = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class review(models.Model):
    reviewid = models.AutoField(primary_key=True)
    review = models.TextField(default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.user) + "="  + self.review[:15] + "..."



class userorder(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)
    order_id = models.IntegerField(default=0)
    o_name = models.CharField(max_length=50,default="")
    o_mobile = models.IntegerField(default=0)
    o_address = models.CharField(max_length=1000,default="")
    o_city = models.CharField(max_length=50,default="")
    o_state = models.CharField(max_length=50,default="")
    o_pin = models.IntegerField(default=0)

    def __str__(self):
        return str(self.o_name) + "-" + str(self.date)