from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Ann_table(models.Model):
    subject = models.CharField(max_length=200)
    message = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='ann_images/')
    visible_to = models.ManyToManyField(User, through='AnnMarkRead')
    #is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    
    '''def is_read_by_user(self, user):
        return AnnMarkRead.objects.filter(announcement=self, user=user, is_read=True).exists()'''
    


    

class AnnMarkRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #visible_to = models.ManyToManyField(User)
    announc = models.ForeignKey(Ann_table, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    

'''class AnnUserRead(models.Model):
    user_read = models.OneToOneField(AnnMarkRead, on_delete=models.CASCADE)
    announc_read = models.ForeignKey(Ann_table, on_delete=models.CASCADE) 
    is_read = models.BooleanField(default=False) '''                        


'''class AnnMarkRead(models.Model):
    announcement = models.ForeignKey('Ann_table', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

class Ann_table(models.Model):
    subject = models.CharField(max_length=200)
    message = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='ann_images/')
    visible_to = models.ManyToManyField(User, related_name='visible_announcements')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    def is_read_by_user(self, user):
        return AnnMarkRead.objects.filter(announcement=self, user=user, is_read=True).exists()'''
