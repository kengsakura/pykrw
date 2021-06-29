from django import forms
from django.db import models
from django.contrib.auth.models import User,auth
from django.db.models import fields
from PIL import Image
from .models import Member,Baseschooldata,Majoractivity,Minoractivity,MinorObjective,MinorIntroduction,MinorGoal,MinorOperation,MinorCost,MinorEvaluation,MinorBenefit,Usemoney\
    ,Numberofuse
from student.models import Room
class Basedata(forms.ModelForm):
    class Meta:
        model = Baseschooldata
        exclude = ['id']
        labels = {
            'type_dta' : 'ประเภท',
            'order' : 'ที่',
            'value' : 'ค่า'
        }
class Roomform(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ['id']
        labels = {
            
            'classroom':'ระดับชั้น',
            'room':'ห้อง',
        }
        widgets = {
            'classroom':forms.NumberInput(attrs={'class':'form-control','required':True}),
            'room':forms.NumberInput(attrs={'class':'form-control','required':True})
        }
class Usemoneyform(forms.ModelForm):
    class Meta:
        model = Usemoney
        exclude = ['id','date','timestamp','minor_id','no','total']
        fields= ['detail','money','count','unit']
        labels = {
            
            'detail':'รายละเอียด',
            'count':'จำนวน',
            'unit':'หน่วย',
            'money':'ราคาต่อหน่วย' 
        }
        
        widgets = {
            'detail':forms.Textarea(attrs={'class':'form-control','cols':'30','rows':'2','required':True}),
            'count':forms.NumberInput(attrs={'class':'form-control','required':True}),
            'unit':forms.TextInput(attrs={'class':'form-control'}),
            'money':forms.NumberInput(attrs={'class':'form-control','required':True})
        }
class Numberofuseform(forms.ModelForm):
    class Meta:
        model = Numberofuse
        exclude = ['id','minor_id','money','status']
        labels = {
            'no':'ครั้งที่',
            'date':'วันที่',
            'type_money':'ประเภทเงิน'
        }
        type_of_money = [('','...เลือก...'),('อุดหนุน','เงินอุดหนุน'),('พัฒนาคุณภาพผู้เรียน','เงินพัฒนาคุณภาพผู้เรียน'),('รายได้สถานศึกษา','เงินรายได้สถานศึกษา')]
        widgets = {
            'type_money':forms.Select(choices=type_of_money,attrs={'class':'form-select','required':True}),
            'no':forms.NumberInput(attrs={'class':'form-control','required':True}),
            'date':forms.DateInput(attrs={'type':'date','class':'form-control','required':True})
        }
class Pictureform(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    class Meta:
        model = Member
        fields = ('image_file', 'x', 'y', 'width', 'height', )
        labels = {
            'image_file':'รูปประจำตัว',
        }

    

class Memberform(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ['id','level','password','image_file','classroom','room']
        labels = {
            'title' : 'คำนำหน้า',
            'fname' : 'ชื่อ',
            'lname' : 'นามสกุล',
            'nickname' : 'ชื่อเล่น',
            'th_id' : 'เลขประจำตัวประชาชน',
            'b_date' : 'วันเดือนปีเกิด',
            'group': 'กลุ่มสาระฯ',
            'tel' : 'โทรศัพท์',
            'username' : 'ชื่อผู้ใช้',
            'email' : 'อีเมลล์',
            'status' : 'สถานะ',
            'date_start' : 'วันที่บรรจุ',
        }
        title_name = [('','...เลือก...'),('นาย','นาย'),('นางสาว','นางสาว'),('นาง','นาง'),('ว่าที่ร้อยตรีหญิง','ว่าที่ร้อยตรีหญิง')]
        group_name = [('','...เลือก...'),('ภาษาไทย','ภาษาไทย'),('คณิตศาสตร์','คณิตศาสตร์'),('วิทยาศาสตร์และเทคโนโลยี','วิทยาศาสตร์และเทคโนโลยี'),('สุขศึกษา','สุขศึกษา'),('สังคมศึกษา','สังคมศึกษา'),('ศิลปะ','ศิลปะ'),('การงานอาชีพ','การงานอาชีพ'),('ภาษาต่างประเทศ','ภาษาต่างประเทศ'),('other','อื่น ๆ')]
        required = {
            'nickname':False
        }
        widgets = {
            'title':forms.Select(choices=title_name,attrs={'class':'form-control'}),
            'fname':forms.TextInput(attrs={'class':'form-control'}),
            'lname':forms.TextInput(attrs={'class':'form-control'}),
            'nickname':forms.TextInput(attrs={'class':'form-control'}),
            'tel':forms.TextInput(attrs={'class':'form-control'}),
            'th_id':forms.TextInput(attrs={'class':'form-control'}),
            'date_start': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'b_date': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'group':forms.Select(choices=group_name,attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'status':forms.TextInput(attrs={'class':'form-control'}),
        }
class Majorform(forms.ModelForm):
    class Meta:
        model = Majoractivity
        exclude = ['id']
        labels = {'name':'ชื่อโครงการ',
            'responsible':'ผู้รับผิดชอบ',
            'money':'จำนวนเงิน',
        }
class Minorform(forms.ModelForm):
    class Meta:
        #ref1 = Baseschooldata.objects.filter(type_dta='ref1').values_list('order','value')
        #ref2 = Baseschooldata.objects.filter(type_dta='ref2').values_list('order','value')
        #ref3 = Baseschooldata.objects.filter(type_dta='ref3').values_list('order','value')
        ref1 = []
        ref2 = []
        ref3 = []
        _ref1 = list(ref1)
        _ref2 = list(ref2)
        _ref3 = list(ref3)
        _ref1.insert(0,('','...เลือก...'))
        _ref2.insert(0,('','...เลือก...'))
        _ref3.insert(0,('','...เลือก...'))
        print(_ref3)
        _year = [('2564','2564'),('2565','2565'),('2566','2566')]
        _detail = [('','...เลือก...'),('กิจกรรมต่อเนื่อง','กิจกรรมต่อเนื่อง'),('กิจกรรมใหม่','กิจกรรมใหม่')]        
        model = Minoractivity
        exclude = ['id','cutoff','money_ask','money','money_1','money_2','money_3']
        labels = {
            'major_id':'เลขโครงการ',
            'year':'ปีการศึกษา',
            'date':'วันที่',
            'name':'ชื่อกิจกรรม',
            'responsible':'ผู้รับผิดชอบ', 
            'branch':'หน่วยงานที่รับผิดชอบ',
            'date_start':'วันที่เริ่ม',
            'date_end':'วันที่สิ้นสุด',
            'detail':'ลักษณะของกิจกรรม',
            #'money':'จำนวนเงิน', 
            'ref1':'กลยุทธ์สพฐ.',
            'ref2':'กลยุทธ์สถานศึกษา',
            'ref3':'มาตรฐานการศึกษาขั้นพื้นฐาน',
        }
        widgets = {
            'major_id':forms.NumberInput(attrs={'class':'form-control'}),
            'year':forms.Select(choices=_year,attrs={'class':'form-select'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'branch':forms.TextInput(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'date_start': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'date_end': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'detail':forms.Select(choices=_detail,attrs={'class':'form-select'}),
            'responsible':forms.TextInput(attrs={'class':'form-control'}),
            #'money':forms.NumberInput(attrs={'class':'form-control'}),
            'ref1':forms.Select(choices=_ref1,attrs={'class':'form-select'}),
            'ref2':forms.Select(choices=_ref2,attrs={'class':'form-select'}),
            'ref3':forms.Select(choices=_ref3,attrs={'class':'form-select'}),
        }
class Introform(forms.ModelForm):
    class Meta:
        model = MinorIntroduction
        exclude = ['id','minor_id']
        labels = {
            'order':'ย่อหน้าที่',
            'detail':'รายละเอียด',
        }
        widgets = {
            'order':forms.NumberInput(attrs={'class':'form-control'}),
            'detail':forms.Textarea(attrs={'class':'form-control','cols':'30','rows':'3'})
        }
class Objectiveform(forms.ModelForm):
    class Meta:
        model = MinorObjective
        exclude = ['id','minor_id']
        labels = {
            'order':'ข้อที่',
            'detail':'รายละเอียด',
        }
        widgets = {
            'order':forms.NumberInput(attrs={'class':'form-control'}),
            'detail':forms.Textarea(attrs={'class':'form-control','cols':'30','rows':'3'})
        }
class Goalform(forms.ModelForm):
    class Meta:
        model = MinorGoal
        exclude = ['id','minor_id']
        labels = {
            'type_goal':'ประเภท',
            'order':'ข้อที่',
            'detail':'รายละเอียด'
        }
        widgets = {
            'type_goal':forms.Select(choices=[('','...เลือก...'),('เชิงคุณภาพ','เชิงคุณภาพ'),('เชิงปริมาณ','เชิงปริมาณ')],attrs={'class':'form-select'}),
            'order':forms.NumberInput(attrs={'class':'form-control'}),
            'detail':forms.Textarea(attrs={'class':'form-control','cols':'30','rows':'2'})
        }
class Operationform(forms.ModelForm):
    class Meta:
        model = MinorOperation
        fields=['type_op','order','detail','date','responsible']
        labels = {
            'type_op':'ประเภท',
            'order':'ข้อที่',
            'detail':'รายละเอียด',
            'date':'วันที่',
            'responsible':'ผู้รับผิดชอบ' 
        }
        widgets = {
            'type_op':forms.Select(choices=[('','...เลือก...'),('ขั้นเตรียมงาน','ขั้นเตรียมงาน'),('ขั้นดำเนินการ','ขั้นดำเนินการ'),('ขั้นตรวจสอบ','ขั้นตรวจสอบ'),('ขั้นรายงาน','ขั้นรายงาน')],attrs={'class':'form-select'}),
            'order':forms.NumberInput(attrs={'class':'form-control'}),
            'responsible':forms.TextInput(attrs={'class':'form-control'}),
            'date':forms.TextInput(attrs={'class':'form-control'}),
            'detail':forms.Textarea(attrs={'class':'form-control','cols':'30','rows':'2'})
        }
class Costform(forms.ModelForm):
    class Meta:
        model = MinorCost
        exclude = ['id','minor_id','totalmoney']
        labels = {
            'order':'ข้อที่',
            'detail':'รายละเอียด',
            'count':'จำนวน',
            'unit':'หน่วย',
            'money':'จำนวนเงิน' 
        }
        widgets = {
            'order':forms.NumberInput(attrs={'class':'form-control'}),
            'detail':forms.Textarea(attrs={'class':'form-control','cols':'30','rows':'2'}),
            'count':forms.NumberInput(attrs={'class':'form-control'}),
            'unit':forms.TextInput(attrs={'class':'form-control'}),
            'money':forms.NumberInput(attrs={'class':'form-control'})
        }
class Evaform(forms.ModelForm):
    class Meta:
        model = MinorEvaluation
        exclude = ['id','minor_id','totalmoney']
        labels = {
            'type_ev':'ประเภท',
            'order':'ข้อที่',
            'detail':'รายละเอียด',
            'criteria':'เกณฑ์',
            'method':'วิธีประเมิน',
            'measure':'เครื่องมือ' 
        }
        widgets = {
            'type_ev':forms.Select(choices=[('','...เลือก...'),('ผลผลิต','ผลผลิต'),('ผลลัพธ์','ผลลัพธ์')],attrs={'class':'form-select'}),
            'order':forms.NumberInput(attrs={'class':'form-control'}),
            'detail':forms.Textarea(attrs={'class':'form-control','cols':'30','rows':'2'}),
            'criteria':forms.NumberInput(attrs={'class':'form-control'}),
            'method':forms.TextInput(attrs={'class':'form-control'}),
            'measure':forms.TextInput(attrs={'class':'form-control'})
        }
class Benefitform(forms.ModelForm):
    class Meta:
        model = MinorBenefit
        exclude = ['id','minor_id']
        labels = {
            'order':'ข้อที่',
            'detail':'รายละเอียด',
        }
        widgets = {
            'order':forms.NumberInput(attrs={'class':'form-control'}),
            'detail':forms.Textarea(attrs={'class':'form-control','cols':'30','rows':'3'})
        }