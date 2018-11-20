from django.db import models
from django.utils import timezone
# Create your models here.


class Applicant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    code = models.CharField(max_length=6)
    current = models.CharField(max_length=5)
    expected = models.CharField(max_length=5)
    date = models.DateTimeField(default=timezone.now)

class Email(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message= models.CharField(max_length=100000)
    def __unicode__(self):
        return self.name
