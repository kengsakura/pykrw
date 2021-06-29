from django.db import models
import datetime
from PIL import Image
from io import BytesIO
import os
from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.
class Baseschooldata(models.Model):
    id = models.AutoField(primary_key=True)
    type_dta = models.CharField(max_length=50,null=True,blank=True)
    order = models.IntegerField(null=True,blank=True)
    value = models.CharField(max_length=200,null=True,blank=True)
    class Meta:
        ordering=('id',)
        verbose_name = 'ข้อมูลหลักโรงเรียน'
        verbose_name_plural = 'ข้อมูลหลักโรงเรียน'
    def __str__(self):
        return self.type_dta+" / "+str(self.order)
class Member(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30,null=True,blank=True)
    th_id = models.CharField(max_length=13,unique=True,null=True,blank=True)
    b_date = models.DateField(null=True,blank=True)
    group = models.CharField(max_length=50,null=True,blank=True)
    tel = models.CharField(max_length=15,null=True,blank=True)
    username = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=100,null=True,blank=True)
    status = models.CharField(null=True,blank=True,max_length=20)
    date_start = models.DateField(null=True,blank=True)
    level = models.CharField(null=True,blank=True,max_length=20)
    image_file = models.ImageField(upload_to="profile/", blank=True, null=True,default = 'profile/blank_profile.png')
    classroom = models.IntegerField(null=True,blank=True)
    room = models.IntegerField(null=True,blank=True)
    class Meta:
        ordering=('id',)
        verbose_name = 'สมาชิก'
        verbose_name_plural = 'ข้อมูลสมาชิก'
    file_format = 'JPEG'
    file_name = ''
    content_type = 'image/jpeg'
    x = 0
    y = 0
    width = 0
    height = 0
    how = 'add'
    def save(self,*args, **kwargs):
        if (self.image_file) and (self.how == 'addpic'):
            bio = BytesIO(self.image_file.read())
            img = Image.open(bio)
            max_size = (320,400)
            x = float(self.x)
            y = float(self.y)
            w = float(self.width)
            h = float(self.height)
            cropped_image = img.crop((x, y, w+x, h+y))
            resized_image = cropped_image.resize(max_size, Image.ANTIALIAS)
            buffer = BytesIO()
            resized_image.save(buffer,self.file_format,quality = 95)
            buffer.seek(0)
            self.image_file = InMemoryUploadedFile(
                buffer,
                'ImageField',
                self.file_name,
                self.content_type,
                buffer.__sizeof__,
                None
            )
        super (Member,self).save(*args, **kwargs)


class Majoractivity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    responsible = models.CharField(max_length=30,null=True,blank=True)
    money = models.DecimalField(max_digits=15,decimal_places=2,null=True,blank=True)
    class Meta:
        verbose_name = 'โครงการ'
        verbose_name_plural = 'ข้อมูลโครงการ'
        ordering=('id',)
class Minoractivity(models.Model):
    id = models.AutoField(primary_key=True)
    major_id = models.IntegerField(default='0',null=True,blank=True)
    year = models.IntegerField(default='2564') 
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    responsible = models.CharField(max_length=30,null=True,blank=True) 
    branch = models.CharField(max_length=30)
    date_start = models.DateField(null=True,blank=True)
    date_end = models.DateField(null=True,blank=True)
    detail = models.CharField(max_length=30)
    money = models.DecimalField(max_digits=15,decimal_places=2)
    money_1 = models.DecimalField(max_digits=15,decimal_places=2,default=0) 
    money_2 = models.DecimalField(max_digits=15,decimal_places=2,default=0) 
    money_3 = models.DecimalField(max_digits=15,decimal_places=2,default=0) 
    ref1 = models.CharField(max_length=100,null=True,blank=True)
    ref2 = models.CharField(max_length=100,null=True,blank=True)
    ref3 = models.CharField(max_length=100,null=True,blank=True)
    cutoff = models.DecimalField(max_digits=15,decimal_places=2,null=True,blank=True) 
    money_ask = models.DecimalField(max_digits=15,decimal_places=2,null=True,blank=True)  
    class Meta:
        ordering=('id',)
        verbose_name = 'กิจกรรม'
        verbose_name_plural = 'ข้อมูลกิจกรรม'
class MinorIntroduction(models.Model):
    id = models.AutoField(primary_key=True)
    minor_id = models.IntegerField(null=True,blank=True)
    order = models.IntegerField()
    detail = models.CharField(max_length=2000)
    class Meta:
        ordering=('id',)
        verbose_name = 'หลักการและเหตุผล'
        verbose_name_plural = 'หลักการและเหตุผล'
class MinorObjective(models.Model):
    id = models.AutoField(primary_key=True)
    minor_id = models.IntegerField(null=True,blank=True)
    order = models.IntegerField()
    detail = models.CharField(max_length=200)
    class Meta:
        ordering=('id',)
        verbose_name = 'วัตถุประสงค์'
        verbose_name_plural = 'วัตถุประสงค์'
class MinorGoal(models.Model):
    id = models.AutoField(primary_key=True)
    minor_id = models.IntegerField()
    type_goal = models.CharField(max_length=20)
    order = models.IntegerField()
    detail = models.CharField(max_length=200)
    class Meta:
        ordering=('id',)
        verbose_name = 'เป้าหมาย'
        verbose_name_plural = 'เป้าหมาย'
class MinorOperation(models.Model):
    id = models.AutoField(primary_key=True)
    minor_id = models.IntegerField()
    type_op = models.CharField(max_length=20)
    order = models.IntegerField()
    date = models.CharField(max_length=100)
    responsible = models.CharField(max_length=100)
    detail = models.CharField(max_length=300)
    class Meta:

        ordering=('id',)
        verbose_name = 'การดำเนินการ'
        verbose_name_plural = 'การดำเนินการ'
class MinorCost(models.Model):
    id = models.AutoField(primary_key=True)
    minor_id = models.IntegerField()
    order = models.IntegerField()
    detail = models.CharField(max_length=200)
    count = models.IntegerField()
    unit = models.CharField(max_length=20)
    money = models.DecimalField(max_digits=15,decimal_places=2)  
    totalmoney = models.DecimalField(max_digits=15,decimal_places=2,null=True,blank=True,default=0)  
    class Meta:
        ordering=('id',)
        verbose_name = 'รายการใช้เงิน'
        verbose_name_plural = 'รายการใช้เงิน'
class MinorEvaluation(models.Model):
    id = models.AutoField(primary_key=True)
    minor_id = models.IntegerField()
    type_ev = models.CharField(max_length=20)
    order = models.IntegerField()
    detail = models.CharField(max_length=200)
    criteria = models.DecimalField(max_digits=5,decimal_places=2)
    method = models.CharField(max_length=200,null=True,blank=True)
    measure = models.CharField(max_length=200,null=True,blank=True)
    class Meta:
        ordering=('id',)
        verbose_name = 'การประเมินผล'
        verbose_name_plural = 'การประเมินผล'
class MinorBenefit(models.Model):
    id = models.AutoField(primary_key=True)
    minor_id = models.IntegerField()
    order = models.IntegerField()
    detail = models.CharField(max_length=200)
    class Meta:
        ordering=('id',)
        verbose_name = 'ผลที่คาดว่าจะได้รับ'
        verbose_name_plural = 'ผลที่คาดว่าจะได้รับ'
class Numberofuse(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    minor_id = models.CharField(max_length=100,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    money = models.DecimalField(max_digits=15,decimal_places=2,null=True,blank=True)
    no = models.IntegerField(null=True,blank=True)
    type_money = models.CharField(max_length=100,null=True,blank=True)
    status = models.CharField(max_length=100,null=True,blank=True,default='0')

class Usemoney(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    date = models.DateField(auto_now_add=True)
    no = models.IntegerField(null=True,blank=True)
    minor_id = models.CharField(max_length=100,null=True,blank=True)
    money = models.DecimalField(max_digits=15,decimal_places=2)
    total = models.DecimalField(max_digits=15,decimal_places=2,default=0)
    detail = models.TextField()
    unit = models.CharField(max_length=100)
    count = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
