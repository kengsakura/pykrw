from django import forms
from django.db import models
from django.contrib.auth.models import User,auth
from django.db.models import fields
from .models import Education,Rank,Documents
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

class Rankform(forms.ModelForm):
    class Meta:
        model = Rank
        fields= ['level','rank','rank_name','date']
        labels = {
            'level':'ตำแหน่ง',
            'rank':'วิทยฐานะ',
            'rank_name':'ชื่อวิทยฐานะ',
            'date':'วันที่ได้รับ'
        }
        rank = [('','...เลือก...'),('ไม่มี','ไม่มี'),('คศ.1','คศ.1'),('คศ.2','คศ.2'),('คศ.3','คศ.3'),('คศ.4','คศ.4'),('คศ.5','คศ.5')]
        rank_name = [('','...เลือก...'),('ไม่มี','ไม่มี'),('ชำนาญการ','ชำนาญการ'),('ชำนาญการพิเศษ','ชำนาญการพิเศษ'),('เชี่ยวชาญ','เชี่ยวชาญ'),('เชี่ยวชาญพิเศษ','เชี่ยวชาญพิเศษ')]
        level = [('','...เลือก...'),('ครูผู้ช่วย','ครูผู้ช่วย'),('ครู','ครู'),('ผู้อำนวยการโรงเรียน','ผู้อำนวยการโรงเรียน'),('รองผู้อำนวยการโรงเรียน','รองผู้อำนวยการโรงเรียน'),('พนักงานราชการ','พนักงานราชการ')]
        widgets = {
            'level':forms.Select(choices=level,attrs={'class':'form-select'}),
            'rank':forms.Select(choices=rank,attrs={'class':'form-select'}),
            'rank_name':forms.Select(choices=rank_name,attrs={'class':'form-select'}),
            'date':forms.DateInput(attrs={'type':'date','class':'form-control','required':True})
        }
class Educationform(forms.ModelForm):
    class Meta:
        model = Education
        fields= ['degree','qualification','initials','major','minor','institution','year_end']
        labels = {
            'degree':'ระดับการศึกษา',
            'qualification':'วุฒิการศึกษา',
            'initials':'ตัวย่อ',
            'major':'คณะ',
            'minor':'สาขา',
            'institution':'สถาบัน',
            'year_end':'ปีที่จบ'
            }
        degree = [('','...เลือก...'),('ปริญญาตรี','ปริญญาตรี'),('ปริญญาโท','ปริญญาโท'),('ปริญญาเอก','ปริญญาเอก'),('อื่น ๆ','อื่น ๆ')]
        widgets = {
            'degree':forms.Select(choices=degree,attrs={'class':'form-select'}),
            'qualification':forms.TextInput(attrs={'class':'form-control'}),
            'initials':forms.TextInput(attrs={'class':'form-control'}),
            'major':forms.TextInput(attrs={'class':'form-control'}),
            'minor':forms.TextInput(attrs={'class':'form-control'}),
            'institution':forms.TextInput(attrs={'class':'form-control'}),
            'year_end':forms.NumberInput(attrs={'class':'form-control','required':True})
        }
class Documentform(forms.ModelForm):
    class Meta:
        model = Documents
        fields= ['type_doc','doc_file']
        labels = {
            'type_doc':'ประเภทเอกสาร',
            'doc_file':'เอกสาร'
            }
        type_doc = [('','...เลือก...'),('สำเนาบัตรประชาชน','สำเนาบัตรประชาชน'),('สำเนาทะเบียนบ้าน','สำเนาทะเบียนบ้าน'),('สำเนาใบประกอบวิชาชีพครู','สำเนาใบประกอบวิชาชีพครู'),('สำเนาใบประกอบวิชาชีพผู้บริหาร','สำเนาใบประกอบวิชาชีพผู้บริหาร')\
            ,('สำเนาวุฒิการศึกษา','สำเนาวุฒิการศึกษา')]
        widgets = {
            'type_doc':forms.Select(choices=type_doc,attrs={'class':'form-select','required':True}),
        }