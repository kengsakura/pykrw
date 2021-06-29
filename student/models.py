from django.db import models
import datetime
from PIL import Image
from io import BytesIO
import os
from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    classroom = models.IntegerField(null=True,blank=True)
    room = models.IntegerField(null=True,blank=True)
    
class Studentdata(models.Model):
    id = models.AutoField(primary_key=True)
    st_id = models.CharField(max_length=20,unique=True)
    title = models.CharField(max_length=20)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30,null=True,blank=True)
    sex = models.CharField(max_length=30)
    th_id = models.CharField(max_length=13,null=True,blank=True)
    b_date = models.DateField(null=True,blank=True)
    classroom = models.IntegerField(null=True,blank=True)
    room = models.IntegerField(null=True,blank=True)
    tel = models.CharField(max_length=15,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    status = models.CharField(null=True,blank=True,max_length=20)
    address = models.TextField(null=True,blank=True)
    class Meta:
        ordering=('id',)
        verbose_name = 'นักเรียน'
        verbose_name_plural = 'ข้อมูลนักเรียน'

class Checkname(models.Model):
    id = models.AutoField(primary_key=True)
    st_id = models.CharField(max_length=20)
    sem = models.IntegerField(null=True,blank=True)
    year = models.IntegerField(null=True,blank=True)
    subject = models.CharField(max_length=100,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    classroom = models.IntegerField(null=True,blank=True)
    room = models.IntegerField(null=True,blank=True)
    status = models.CharField(null=True,blank=True,max_length=20)

