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
    profile_pic = models.ImageField(upload_to='profile-pic/uploads/%y/%m/%d', default='user-avatar-placeholder.png', blank=True, null=True)
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