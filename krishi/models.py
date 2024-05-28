from django.db import models
from django.db import models
from django.utils import timezone
from account.models import User

# Create your models here.
class item(models.Model):
    img=models.ImageField(upload_to='pics')
    name=models.CharField(max_length=100)
    show=models.BooleanField(default=False)
    def __str__(self):
        return self.name

class selling(models.Model):
    username=models.CharField(max_length=100,default="unknown")
    img=models.ImageField (upload_to='sellimg')
    product=models.CharField(max_length=100)
    productdet=models.CharField(max_length=100)
    quantity=models.CharField(max_length=100)
    price=models.IntegerField()
    phone=models.CharField(max_length=100)
    email=models.EmailField()
    def __str__(self):
        return self.username
    
class PlantResult(models.Model):
    name=models.CharField(max_length=100)
    name2=models.CharField(max_length=100)
    cause=models.TextField(default=None)
    symptoms=models.TextField(default=None)
    life_cycle=models.TextField(default=None)
    prevention_and_control=models.TextField(default=None)
    def __str__(self):
        return self.name
    
class feedback(models.Model):
    message=models.TextField()
    first_name=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    email=models.EmailField()
    def __str__(self):
        return self.email

class counsel(models.Model):
    first_name=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    phone=models.CharField(max_length=10)
    postal_code=models.CharField(max_length=10)
    local_address=models.TextField()
    type=models.CharField(max_length=100,default="general counselling")
    email=models.EmailField()
    date=models.DateField(default='2023-04-01')
    def __str__(self):
        return self.state
    

class newsletter(models.Model):
    email=models.EmailField()
    def __str__(self):
        return self.email

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='detection')

class Policy(models.Model):
    POLICY_TYPE_CHOICES = (
        ('Government', 'Government'),
        ('Private', 'Private'),
        # Add more choices as needed
    )

    policy_type = models.CharField(max_length=50, choices=POLICY_TYPE_CHOICES)
    policy_name = models.CharField(max_length=100)
    policy_content=models.TextField(default="Not Available")
    policy_link=models.TextField(default="Not Available")
    def __str__(self):
        return self.policy_name

class AgriculturalSite(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    description = models.TextField()
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    price = models.IntegerField()
    def __str__(self):
        return self.name

class SiteImage(models.Model):
    site = models.ForeignKey(AgriculturalSite, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='site_images')

    def __str__(self):
        return f"Image for {self.site.name}"
    

class FaQ(models.Model):
    question=models.TextField(default="Not Available")
    answer=models.TextField(default="Not Available")
    def __str__(self):
        return self.question
