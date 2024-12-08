from django.db import models

# Create your models here.

class EmailSetup(models.Model):
    smtp_server_address = models.CharField(max_length=250)  #EMAIL_HOST
    email_address = models.EmailField(max_length=250)
    password = models.CharField(max_length=250) #app password
    port = models.PositiveIntegerField()
    required_authentication = models.BooleanField(default = True)
    security = models.CharField(max_length = 200,choices = (('None','None'),('SSL','SSL'),('TSL','TSL')),default = 'None')
    smtp_username = models.CharField(max_length = 100,null = True,blank = True)
    verify_smtp_certificate = models.BooleanField(default = False)
    
    def __str__(self):
        return f"{self.email_address}: {self.smtp_server_address} -> {self.port}"
    
    class Meta:
        permissions=[
            ('manage_email_setup','Manage Email Setup')
        ]
