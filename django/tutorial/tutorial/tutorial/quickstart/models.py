from django.db import models

class Task(models.Model):
    task_name = models.CharField(max_length=30)
    task_desc = models.CharField(max_length=30)
    image = models.ImageField(upload_to='pic_folder/', default='pic_folder/None/no-img.jpg')


# Create your models here.
