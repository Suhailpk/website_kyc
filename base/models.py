from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username

def file_size(value): # add this to some file where you can import it from
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 5 MiB.')   

class Kyc(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=50)
    address = models.TextField()
    passport = models.FileField(upload_to='kyc_documents/',validators=[file_size])
    aadhaar = models.FileField(upload_to='kyc_documents/',validators=[file_size])
    driving_license = models.FileField(upload_to='kyc_documents/',validators=[file_size])
    approved = models.BooleanField(default=False)
    waiting = models.BooleanField(default=False)
    submitted= models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.full_name
    









