from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Ann_table(models.Model):
    subject = models.CharField(max_length=200)
    message = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    image = models.ImageField(upload_to='ann_images/')
    visible_to = models.ManyToManyField(User, through='AnnMarkRead')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    
    


    

class AnnMarkRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announc = models.ForeignKey(Ann_table, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    

