from django.db import models
import datetime
from PIL import Image
from io import BytesIO
import os
import random
from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile


class Education(models.Model):
    id = models.AutoField(primary_key=True)
    teacher_id = models.CharField(max_length=13,null=True,blank=True)
    th_id = models.CharField(max_length=13,null=True,blank=True)
    degree = models.CharField(max_length=50,null=True,blank=True)
    major = models.CharField(max_length=100,null=True,blank=True)
    minor = models.CharField(max_length=100,null=True,blank=True)
    qualification = models.CharField(max_length=100,null=True,blank=True)
    initials = models.CharField(max_length=100,null=True,blank=True)
    institution = models.CharField(max_length=300,null=True,blank=True)
    year_end = models.CharField(max_length=100,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
class Rank(models.Model):
    id = models.AutoField(primary_key=True)
    teacher_id = models.CharField(max_length=13,null=True,blank=True)
    th_id = models.CharField(max_length=13,null=True,blank=True)
    level = models.CharField(max_length=100,null=True,blank=True)
    rank = models.CharField(max_length=100,null=True,blank=True)
    rank_name = models.CharField(max_length=100,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Documents(models.Model):
    id = models.AutoField(primary_key=True)
    teacher_id = models.CharField(max_length=13,null=True,blank=True)
    type_doc = models.CharField(max_length=100,null=True)
    doc_file = models.FileField(upload_to="documents/",null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

'''
def get_unique_name(dir,filename,type):
        if not dir.endswith('/'):
            dir+='/'
        if os.path.exists(f'{dir}{filename}'):
            sp = filename.split('.',1)
            name = type
            ext = sp[1]
            r = random.randint(1000,10000)
            return f'{name}_{r}.{ext}'
        else:
            return filename

def save_file(dir,file):
    if not dir.endswith('/'):
        dir+='/'
    with open(f'{dir}{file.name}','wb+') as target:
        for chunk in file.chunks():
            target.write(chunk)
'''
class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id  = models.CharField(max_length=10,null=True,blank=True)
    name  = models.CharField(max_length=100,null=True,blank=True)
    group = models.CharField(max_length=100,null=True,blank=True)
    teacher_id = models.CharField(max_length=13,null=True,blank=True)
    unit = models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=10)
    classroom = models.IntegerField(null=True,blank=True)
    room = models.IntegerField(null=True,blank=True)
