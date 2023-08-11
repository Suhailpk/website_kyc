from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Ann_table(models.Model):
    subject = models.CharField(max_length=200)
    message = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='ann_images/')
    visible_to = models.ManyToManyField(User, related_name='visible_announcements')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

