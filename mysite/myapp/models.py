from typing import Tuple
from django.db import  models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import AutoField
from django.urls import reverse
from django.utils import timezone
# Create your models here.

class commentModel_1(models.Model):
    author = models.ForeignKey('auth.User' ,on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    published_date =models.DateTimeField(default=timezone.now)
    # question = models.CharField(max_length=578,blank=True,null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        
        return self.author.username

    def get_absolute_url(self):
        print(self.pk)
        return reverse("electronic", kwargs={"pk": self.pk})
    
class userProfileModel(models.Model):
    name = models.OneToOneField('auth.User',on_delete=models.CASCADE)
    # phone_no = models.CharField()
    userpic =models.ImageField(upload_to= 'pic',blank=True,null=True) 
    

    def __str__(self):
        return self.name.username   

    

class questionModel(models.Model):
    user_name = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    question = models.CharField(max_length=578)
    answer = models.CharField( max_length=500)
   

    def __str__(self):
        return self.user_name.username

class ProductModel(models.Model):
    catagory = models.CharField(max_length=256)
    slug  = models.SlugField(null=True,blank=True)

    def __str__(self):
        return self.catagory


class itemModel(models.Model):
    item_id  = models.ForeignKey( ProductModel,on_delete=models.CASCADE,null=False)
    item_name = models.CharField(max_length=256)
    item_discription= models.CharField(max_length=1000)
    item_Price= models.IntegerField(null=False,default=100)
    item_offer = models.IntegerField(null=False,default=0)
    in_stoke = models.IntegerField(default=0)
    slug  = models.SlugField(null=True,blank=True)
    sold_by = models.CharField(max_length=126)
    item_image = models.ImageField(upload_to= 'pic',blank=True,null=True)
    LOW = 0
    NORMAL=1
    HIGH=2
    status_choice=[
        (LOW ,'low'),
        (NORMAL,'normal'),
        (HIGH,'high'),
    ]
    quality = models.IntegerField(choices=status_choice,default=NORMAL)

    # def get_absolute_url(self):
    #     return reverse("kitchen", kwargs={"pk":self.pk})

    def __str__(self):
        return self.item_name


class CartUser(models.Model):
    cart_holder=models.ForeignKey(User,on_delete=models.CASCADE,related_name="cart_user_name")



class Cart (models.Model):
    cart_user= models.ForeignKey(CartUser,on_delete=CASCADE)
    cart_product = models.CharField(max_length=200)
    cart_item = models.CharField(max_length=256)
    
    cart_item_quantity = models.IntegerField(default=0)
    cart_item_quality =models.IntegerField(default=0)
    cart_item_price = models.IntegerField()
    

    def __str__(self):
        return self.cart_user.cart_holder.username
    
  
class  Oders(models.Model):
    oder_user = models.CharField(max_length=256)
    mobile_no = models.IntegerField()
    pincode   = models.IntegerField()
    amount   = models.IntegerField()
    
    country   = models.CharField(max_length=256)
    address   = models.CharField(max_length=500)
    landmark   = models.CharField(max_length=256)
    city      = models.CharField(max_length=256)
    state     = models.CharField(max_length=256)
    
    def __str__(self):
        return self.oder_user
    
    











