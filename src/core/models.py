from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize


# Create your models here.
class Profile(models.Model):
    
    ACCOUNT_TYPE = (
        ('supervisor', 'Supervisor'),
        ('cadet', 'Cadet')
    )

    GENDER = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    
    user = models.OneToOneField(User,  related_name='userprofiles', on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(upload_to='profile-pic/uploads/%y/%m/%d', default='avatar.png', blank=True, null=True)
    smart = ImageSpecField(source='profile_pic', processors=[SmartResize(512,512)], format='PNG')
    gender = models.CharField(max_length=50, choices=GENDER)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE, null=True)
    profile_updated = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return "{} Profile".format(self.user)


    class Meta:
        ordering = ('-created',)
        verbose_name_plural = 'Profile'

        
class Cadetlogbook(models.Model):
    
    DEPARTMENT = (
        ('biology', 'Biology'),
        ('chemistry', 'Chemistry'),
        ('computer science', 'Computer Science'),
    )

    WORK_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    work_title = models.CharField(max_length=100, null=True)
    description_of_work = models.TextField() 
    department =  models.CharField(max_length=50, choices=DEPARTMENT, null=True)
    work_status = models.CharField(max_length=200, choices=WORK_STATUS, default='pending')
    end_date  = models.DateField(null=True) 
    comment = models.CharField(max_length=3000, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False) 

    def __str__(self) -> str:
        return "CadetLogbook"

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = 'Cadetlogbook'