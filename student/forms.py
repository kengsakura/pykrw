from django import forms
from django.db import models
from django.contrib.auth.models import User,auth
from django.db.models import fields
from .models import Studentdata,Checkname
from teacher.models import Subject
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

class Checkform(forms.ModelForm):
    class Meta:
        model = Checkname
        fields= ['status']
        labels = {
            'status':'สถานะ'
        }
        select = [('มา',''),('ขาด',''),('ลาป่วย',''),('ลากิจ','')]
        widgets = {
            'status':forms.RadioSelect(choices=select,attrs={'class':'form-control'})
        }
class Subjectform(forms.ModelForm):
    class Meta:
        model = Subject
        exclude= ['id','teacher_id']
        labels = {
            'subject_id':'รหัสวิชา',
            'name' :'ชื่อวิชา', 
            'group':'กลุ่มสาระ',
            'unit' :'หน่วยกิต',
            'classroom' :'ชั้น',
            'room' :'ห้อง',
        }
        group_name = [('','...เลือก...'),('ภาษาไทย','ภาษาไทย'),('คณิตศาสตร์','คณิตศาสตร์'),('วิทยาศาสตร์และเทคโนโลยี','วิทยาศาสตร์และเทคโนโลยี'),('สุขศึกษา','สุขศึกษา'),('สังคมศึกษา','สังคมศึกษา'),('ศิลปะ','ศิลปะ'),('การงานอาชีพ','การงานอาชีพ'),('ภาษาต่างประเทศ','ภาษาต่างประเทศ'),('other','อื่น ๆ')]
        widgets = {
            'group':forms.Select(choices=group_name),
            'unit':forms.NumberInput(attrs={'step':'any'}),
            'classroom':forms.NumberInput(),
            'room':forms.NumberInput(),
        }