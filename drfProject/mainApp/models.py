from django.db import models

# Create your models here.
class ModelTarget(models.Model):
    modelname=models.CharField(max_length=50)
    target=models.TextField()
    result=models.TextField(null=True)
    csv_file=models.FileField(upload_to='csv_files/',null=True,blank=True)
    original_filename = models.CharField(max_length=255, blank=True, null=True)