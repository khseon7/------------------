from django.db import models

# Create your models here.
class Review(models.Model):
    title=models.CharField(max_length=50)
    content=models.TextField()
    updated_at=models.DateTimeField(auto_now=True)

class ModelParameter(models.Model):
    modelname=models.CharField(max_length=50)
    parameter=models.TextField()
    result=models.TextField(null=True)
    csv_file=models.FileField(upload_to='csv_files/',null=True,blank=True)
    updated_at=models.DateTimeField(auto_now=True)