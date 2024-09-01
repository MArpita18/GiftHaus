from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zip = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.address1+", "+self.address2+", "+self.city+", "+self.state+", "+self.country+", "+self.zip+", "+self.mobile
    
