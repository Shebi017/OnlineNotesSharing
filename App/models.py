from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=13,null=True,blank=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,null=True,blank=True)
    choices = [
        ('Student','Student'),
        ('Teacher','Teacher')
    ]
    role = models.CharField(max_length=30,choices=choices,null=True,blank=True)

    def __str__(self):
        return self.user.username + " - " + self.user.email


class Note(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=50)
    file = models.FileField(upload_to="uploaded_file/")
    file_type_choices = [
        ('Text','Text'),
        ('PNG','PNG'),
        ('PPT','PPT'),
    ]
    file_type = models.CharField(max_length=50,choices=file_type_choices)

    description = models.CharField(max_length=50)
    status_choices = [
        ('Pending','Pending'),
        ('Reject','Reject'),
        ('Accept','Accept')
    ]

    status = models.CharField(max_length=50,choices=status_choices,default="Pending")

    def __str__(self):
        return self.profile.user.username + ' - ' + self.subject
    


class Contact(models.Model):
    name = models.CharField(max_length=50)
    phone =  models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=50)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
