from django.db import models
import uuid
from datetime import datetime
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
import uuid
from PIL import Image
from io import BytesIO


class Blood(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='bloods_imgs', null=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(max_length=200, null=True, blank=False)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, blank=False)
    bio = models.TextField(blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{11}$', message="Phone number must be entered in the format: '01234567899'. Up to 11 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=11, blank=False)
    bloodgroups = models.ForeignKey(Blood, on_delete=models.SET_NULL, blank=True, null=True)
    joined = models.DateTimeField(auto_now_add=True)

    avatar = models.ImageField(upload_to='profile_images', null=True, default="avatar.svg")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def compressImage(self, avatar):
        image_file = BytesIO(avatar.file.read())
        n_image = Image.open(image_file)
        n_image.thumbnail((600, 400), Image.ANTIALIAS)
        image_file = BytesIO()
        n_image.save(image_file, 'JPEG')
        return image_file
        
    #def save(self, *args, **kwargs):
     #   if not self.id:
      #      self.avatar = self.compressImage(self.avatar)
       # super(User, self).save(*args, **kwargs)

def set_username(sender, instance, **kwargs):
    username = instance.username.replace(' ', '').lower()
    while User.objects.filter(username=username).exists():
        username = instance.username + '-' + uuid.uuid4().hex[:4]
    instance.username = username.replace(' ', '').lower()
models.signals.pre_save.connect(set_username, sender=User)
    

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=500)

    def __str__(self):
        return self.username


class Division(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100, blank=True)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Donner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, blank=False)
    bloodgroups = models.ForeignKey(Blood, on_delete=models.SET_NULL, blank=False, null=True)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, blank=False, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=False, null=True)
    city = models.CharField(max_length=50, blank=True, default='')
    donation_date = models.DateField(null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{11}$', message="Phone number must be entered in the format: '01234567899'. Up to 11 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=11, blank=False, unique=True)
    updated = models.DateTimeField(auto_now=True)
    status_choice = (
        ('রক্তদাতার তথ্য Mugdhota Blood Bank কর্তৃক যাচাইকৃত', 'রক্তদাতার তথ্য Mugdhota Blood Bank কর্তৃক যাচাইকৃত'),
        ('যাচাইকৃত নয়', 'যাচাইকৃত নয়'),
    )
    status = models.CharField(max_length=100, choices=status_choice, default = 'যাচাইকৃত নয়', blank=True)

    def bloodinfo(self):
        return ",".join('name' 'bloodgroups' 'location' 'phone' 'donation_date' 'status' 'author' 'updated')

    @property
    def image(self):
        return self.bloodgroups.image.url


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    donner = models.ForeignKey(Donner, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
        
        
class Contact(models.Model):
    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{11}$', message="Phone number must be entered in the format: '01234567899'. Up to 11 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=11, blank=False)
    question = models.TextField(max_length=200, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    cntchoice = (
        ('Solved', 'Solved'),
        ('Unsolved', 'Unsolved'),
    )
    cntstatus = models.CharField(max_length=100, choices=cntchoice, default = 'Unsolved', blank=True, null=True)

    
    def contactinfo(self):
        return ",".join('name' 'email' 'location' 'phone' 'question' 'created' 'cntstatus')
    
        
class BloodInfoAddProblem(models.Model):
    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{11}$', message="Phone number must be entered in the format: '01234567899'. Up to 11 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=11, blank=False)
    question = models.TextField(max_length=200, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    biapchoice = (
        ('Solved', 'Solved'),
        ('Unsolved', 'Unsolved'),
    )
    biapstatus = models.CharField(max_length=100, choices=biapchoice, default = 'Unsolved', blank=True, null=True)

    
    def contactinfo(self):
        return ",".join('name' 'email' 'location' 'phone' 'question' 'created' 'biapstatus')


class ManagementRole(models.Model):
    name = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name
        

class Management(models.Model):
    serial_num = models.IntegerField()
    management_role = models.ForeignKey(ManagementRole, on_delete=models.SET_NULL, blank=False, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(blank=True)
    designation = models.CharField(max_length=200, blank=True, null=True)
    social_media = models.CharField(max_length=200, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{11}$', message="Phone number must be entered in the format: '01234567899'. Up to 11 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=11, blank=True)
    bloodgroups = models.ForeignKey(Blood, on_delete=models.SET_NULL, blank=True, null=True)
    #division = models.ForeignKey(Division, on_delete=models.SET_NULL, blank=False, null=True)
    #location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=False, null=True)
    #city = models.CharField(max_length=50, blank=True, default='')
    joined = models.DateTimeField(auto_now_add=True)

    avatar = models.ImageField(upload_to='profile_images', null=True, default="avatar.svg")
    
    def compressImage(self, avatar):
        image_file = BytesIO(avatar.file.read())
        n_image = Image.open(image_file)
        n_image.thumbnail((600, 400), Image.ANTIALIAS)
        image_file = BytesIO()
        n_image.save(image_file, 'JPEG')
        return image_file
        
    def managementdetails(self):
        return ",".join('serial_num' 'name' 'management_role' 'email' 'phone' 'joined')    

