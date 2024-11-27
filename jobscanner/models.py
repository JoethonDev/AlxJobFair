from django.db import models

# Create your models here.
class Recrutier(models.Model):
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    days = models.IntegerField()
    members = models.IntegerField()
    code = models.IntegerField(unique=True)
    
    def __str__(self) :
        return f"{self.name}"

class Freelancer(models.Model):
    email = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    location = models.TextField()
    track = models.CharField(max_length=255)
    job_interest = models.CharField(max_length=255)
    cv_url = models.TextField()
    visits = models.IntegerField(default=0)

    def __str__(self) :
        return f"{self.email} graduated from {self.track} looks for {self.job_interest}"
    
class ScanLog(models.Model):
    recrutier = models.ForeignKey(Recrutier, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    comment = models.TextField()
