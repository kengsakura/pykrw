from PIL.Image import Image
from django.forms.models import ModelMultipleChoiceField
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse, FileResponse
from project.models import Member,Minoractivity,Majoractivity,Numberofuse
from project.forms import Memberform,Pictureform
from .models import Education,Rank,Documents
from .forms import Rankform,Educationform,Documentform
from django.db.models import Avg, Count, Min, Sum,Q, Max,CharField, Value
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse, FileResponse
from django.contrib import messages
from PIL import Image
from bahttext import bahttext
import time
import os
import random
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from teacher import forms
# Create your views here.
def index(request):
    if "user" not in request.session:
        return render(request,'login.html')
    allmoney = Minoractivity.objects.aggregate(Sum('money'))['money__sum']
    if Numberofuse.objects.aggregate(Sum('money'))['money__sum'] == None:
        currentuse = 0
    else:
        currentuse = Numberofuse.objects.aggregate(Sum('money'))['money__sum']
    dashlist = [Majoractivity.objects.all().count(),Minoractivity.objects.count(),allmoney,currentuse]
    if allmoney == None:
        allmoney_text = "ศูนย์"
    else:
        allmoney_text = bahttext(allmoney)
    total_text = bahttext(currentuse)
    data = Member.objects.get(Q(fname = request.session["user"][2])&Q(lname = request.session["user"][3]))
    context = {'dashlist':dashlist,'allmoney':allmoney_text,'total':total_text,'data':data}
    return render(request,'index.html',context)

def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        member = Member.objects.filter(Q(username = username)&Q(password = password))
        if member.exists():
            x = list(list(member.values_list())[0]).copy()
            x[6] = 'nodata'
            x[13] = 'nodata'
            request.session['user'] = x
            request.session['pic'] = 'http://krwplan.s3.amazonaws.com/'+str(member.first().image_file)
            messages.info(request,"เข้าสู่ระบบสำเร็จ")
            return redirect('index')
        else:
            messages.info(request,"ไม่พบข้อมูลในระบบ")
            return redirect('/login/')
    return render(request,'login.html')

def Logout(request):
    if "user" not in request.session:
        return render(request,'login.html')
    del request.session['user']
    del request.session['pic']
    request.session.modified = True
    return render(request,'login.html')

def Profile(request):
    if "user" not in request.session:
        return render(request,'login.html')
    data = Member.objects.get(Q(fname = request.session["user"][2])&Q(lname = request.session["user"][3]))
    if request.method == 'POST':
        
        data2 = Member.objects.get(Q(fname = request.session["user"][2])&Q(lname = request.session["user"][3]))
        #teacher = Member.objects.filter(id = data.id).values_list('th_id')[0][0]
        if request.POST.get('how') == 'addger':
            data_form = Memberform(request.POST,instance=data)
            if data_form.is_valid():
                Member.how = request.POST.get('how')
                data_form.save()
                messages.info(request,'เรียบร้อย')
                print('y')
                return HttpResponseRedirect("/teacher/profile/")
        elif request.POST.get('how') == 'addpic':
            print('n')
            pic_form = Pictureform(request.POST,request.FILES)
            if pic_form.is_valid():
                pic_form = Pictureform(request.POST,request.FILES,instance=data2)
                file = request.FILES['image_file']
                Member.file_format = file.image.format
                Member.file_name = file.name
                Member.content_type = file.content_type
                Member.x = request.POST.get('x')
                Member.y = request.POST.get('y')
                Member.width = request.POST.get('width')
                Member.height = request.POST.get('height')
                Member.how = request.POST.get('how')
                pic_form.save()
                request.session['pic'] = 'http://krwplan.s3.amazonaws.com/profile/'+str(file.name)
                request.session.modified = True
                request.session.save()
                messages.info(request,'เรียบร้อย')
                return HttpResponseRedirect("/teacher/profile/")
        elif request.POST.get('how') == 'addedu':
            education_form = Educationform(request.POST)
            if education_form.is_valid():
                Member.how = request.POST.get('how')
                new_edu = education_form.save(commit=False)
                new_edu.th_id = data.th_id
                new_edu.teacher_id = data.id
                new_edu.save()
                messages.info(request,'เรียบร้อย')
                return HttpResponseRedirect("/teacher/profile/")
        elif request.POST.get('how') == 'addqua':
            rank_form = Rankform(request.POST)
            if rank_form.is_valid():
                Member.how = request.POST.get('how')
                new_rank = rank_form.save(commit=False)
                new_rank.th_id = data.th_id
                new_rank.teacher_id = data.id
                new_rank.save()
                messages.info(request,'เรียบร้อย')
                return HttpResponseRedirect("/teacher/profile/")
        elif request.POST.get('how') == 'rank_edit':
            id = request.POST.get('rid')
            level = request.POST.get('e_level')
            rank = request.POST.get('e_rank')
            rank_name = request.POST.get('e_rank_name')
            date = request.POST.get('e_date')
            rank_data = Rank.objects.filter(id = id).update(
                level = level,
                rank = rank,
                rank_name = rank_name,
                date = date
            )
            messages.info(request,'เรียบร้อย')
            return HttpResponseRedirect("/teacher/profile/")
        elif request.POST.get('how') == 'edu_edit':
            id = request.POST.get('eid')
            degree = request.POST.get('e_degree')
            major = request.POST.get('e_major')
            minor = request.POST.get('e_minor')
            qualification = request.POST.get('e_qualification')
            initials = request.POST.get('e_initials')
            institution = request.POST.get('e_institution')
            year_end = request.POST.get('e_year_end')
            edu_data = Education.objects.filter(id = id).update(
                degree = degree,
                major = major,
                minor = minor,
                qualification = qualification,
                initials = initials,
                institution = institution,
                year_end = year_end
            )
            messages.info(request,'เรียบร้อย')
            return HttpResponseRedirect("/teacher/profile/")
        elif request.POST.get('how') == 'rank_del':
            id = request.POST.get('rid')
            Rank.objects.filter(id = id).delete()
            messages.info(request,'เรียบร้อย')
            return HttpResponseRedirect("/teacher/profile/")
        elif request.POST.get('how') == 'edu_del':
            id = request.POST.get('eid')
            Education.objects.filter(id = id).delete()
            messages.info(request,'เรียบร้อย')
            return HttpResponseRedirect("/teacher/profile/")
    pic_form = Pictureform()
    education = Education.objects.filter(teacher_id = data.id)
    pic = data.image_file
    data_form = Memberform(instance=data)
    education_form = Educationform()
    rank = Rank.objects.filter(teacher_id = data.id)
    rank_form = Rankform()
    doc = Documents.objects.filter(teacher_id = data.id)
    list_doc = ['สำเนาบัตรประชาชน','สำเนาทะเบียนบ้าน','สำเนาใบประกอบวิชาชีพครู','สำเนาใบประกอบวิชาชีพผู้บริหาร','สำเนาวุฒิการศึกษา']
    doc_list = []
    for i in list_doc:
        inside_list = []
        x = doc.filter(type_doc = i)
        inside_list.append(i)
        inside_list.append(x)
        doc_list.append(inside_list)
    today = datetime.date.today()
    if data.b_date:
        age = today.year - data.b_date.year - ((today.month, today.day) < (data.b_date.month, data.b_date.day))
    else:
        age = None
    context = {'data':data,'age':age,'df':data_form,'edu':education_form,'pp':pic_form,'education':education,'pic':pic,'rank':rank,'rank_form':rank_form,'doc_list':doc_list}
    return render(request,'teacher/profile.html',context)

def Allteacher(request):
    if "user" not in request.session:
        return render(request,'login.html')
    all = Member.objects.all()
    edu = Education.objects.all()
    rank = Rank.objects.all()
    for i in all:
        edu_list = edu.filter(teacher_id=i.id).values_list('degree','qualification','initials','major','minor','institution','year_end')
        rank_list = rank.filter(teacher_id=i.id).values_list('level','rank','rank_name','date')
        i.edu_list = edu_list # This line is the problem
        i.rank_list = rank_list
    context = {'all':all}
    return render(request,'teacher/allteacher.html',context)
    
def documents(request):
    if "user" not in request.session:
        return render(request,'login.html')
    user_data = Member.objects.get(id = request.session['user'][0])
    if request.method == 'POST':
        if request.POST.get('how') == 'del':
            id = request.POST.get('id')
            Documents.objects.filter(id = id).delete()
            messages.info(request,'เรียบร้อย')
            return HttpResponseRedirect("/teacher/profile/documents")
        form = Documentform(request.POST,request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.teacher_id = user_data.id
            new.save()
            messages.info(request,'เรียบร้อย')
            return HttpResponseRedirect("/teacher/profile/documents")
    else:
        form = Documentform()
    doc_data = Documents.objects.filter(teacher_id = user_data.id)
    context = {'data':user_data,'doc_data':doc_data,'forms':form}
    return render(request,'teacher/documents.html',context)

def ProfileAdmin(request,pk):
    if "user" not in request.session:
        return render(request,'login.html')
    if not (request.session['user'][14] == '3' or request.session['user'][14] == '4'):
        return redirect('index')
    data = Member.objects.get(id = pk)
    if request.method == 'POST':
        data2 = Member.objects.get(id = pk)
        #teacher = Member.objects.filter(id = data.id).values_list('th_id')[0][0]
        if request.POST.get('how') == 'addger':
            data_form = Memberform(request.POST,instance=data)
            if data_form.is_valid():
                Member.how = request.POST.get('how')
                data_form.save()
                messages.info(request,'เรียบร้อย')
                print('y')
                return HttpResponseRedirect("/teacher/profilead/{}".format(pk))
        elif request.POST.get('how') == 'addpic':
            print('n')
            pic_form = Pictureform(request.POST,request.FILES)
            if pic_form.is_valid():
                pic_form = Pictureform(request.POST,request.FILES,instance=data2)
                file = request.FILES['image_file']
                Member.file_format = file.image.format
                Member.file_name = file.name
                Member.content_type = file.content_type
                Member.x = request.POST.get('x')
                Member.y = request.POST.get('y')
                Member.width = request.POST.get('width')
                Member.height = request.POST.get('height')
                Member.how = request.POST.get('how')
                pic_form.save()
                messages.info(request,'เรียบร้อย')
                return HttpResponseRedirect("/teacher/profilead/{}".format(pk))
        elif request.POST.get('how') == 'addedu':
            education_form = Educationform(request.POST)
            if education_form.is_valid():
                Member.how = request.POST.get('how')
                new_edu = education_form.save(commit=False)
                new_edu.th_id = data.th_id
                new_edu.teacher_id = data.id
                new_edu.save()
                messages.info(request,'เรียบร้อย')
                return HttpResponseRedirect("/teacher/profilead/{}".format(pk))
        elif request.POST.get('how') == 'addqua':
            rank_form = Rankform(request.POST)
            if rank_form.is_valid():
                Member.how = request.POST.get('how')
                new_rank = rank_form.save(commit=False)
                new_rank.th_id = data.th_id
                new_rank.teacher_id = data.id
                new_rank.save()
                messages.info(request,'เรียบร้อย')
                return HttpResponseRedirect("/teacher/profilead/{}".format(pk))
        elif request.POST.get('how') == 'rank_edit':
            id = request.POST.get('rid')
            level = request.POST.get('e_level')
            rank = request.POST.get('e_rank')
            rank_name = request.POST.get('e_rank_name')
            date = request.POST.get('e_date')
            rank_data = Rank.objects.filter(id = id).update(
                level = level,
                rank = rank,
                rank_name = rank_name,
                date = date
            )
            messages.info(request,'เรียบร้อย')
            return HttpResponseRedirect("/teacher/profilead/{}".format(pk))
        elif request.POST.get('how') == 'edu_edit':
            id = request.POST.get('eid')
            degree = request.POST.get('e_degree')
            major = request.POST.get('e_major')
            minor = request.POST.get('e_minor')
            qualification = request.POST.get('e_qualification')
            initials = request.POST.get('e_initials')
            institution = request.POST.get('e_institution')
            year_end = request.POST.get('e_year_end')
            edu_data = Education.objects.filter(id = id).update(
                degree = degree,
                major = major,
                minor = minor,
                qualification = qualification,
                initials = initials,
                institution = institution,
                year_end = year_end
            )
            messages.info(request,'เรียบร้อย')
            return HttpResponseRedirect("/teacher/profilead/{}".format(pk))
        elif request.POST.get('how') == 'rank_del':
            id = request.POST.get('rid')
            Rank.objects.filter(id = id).delete()
            messages.info(request,'เรียบร้อย')
            return HttpResponseRedirect("/teacher/profilead/{}".format(pk))
        elif request.POST.get('how') == 'edu_del':
            id = request.POST.get('eid')
            Education.objects.filter(id = id).delete()
            messages.info(request,'เรียบร้อย')
            return HttpResponseRedirect("/teacher/profilead/{}".format(pk))
    pic_form = Pictureform()
    education = Education.objects.filter(teacher_id = data.id)
    pic = data.image_file
    data_form = Memberform(instance=data)
    education_form = Educationform()
    rank = Rank.objects.filter(teacher_id = data.id)
    rank_form = Rankform()
    doc = Documents.objects.filter(teacher_id = data.id)
    list_doc = ['สำเนาบัตรประชาชน','สำเนาทะเบียนบ้าน','สำเนาใบประกอบวิชาชีพครู','สำเนาใบประกอบวิชาชีพผู้บริหาร','สำเนาวุฒิการศึกษา']
    doc_list = []
    for i in list_doc:
        inside_list = []
        x = doc.filter(type_doc = i)
        inside_list.append(i)
        inside_list.append(x)
        doc_list.append(inside_list)
    today = datetime.date.today()
    if data.b_date:
        age = today.year - data.b_date.year - ((today.month, today.day) < (data.b_date.month, data.b_date.day))
    else:
        age = None
    context = {'data':data,'age':age,'df':data_form,'edu':education_form,'pp':pic_form,'education':education,'pic':pic,'rank':rank,'rank_form':rank_form,'doc_list':doc_list}
    return render(request,'teacher/profilead.html',context)

def documentsAdmin(request,pk):
    if "user" not in request.session:
        return render(request,'login.html')
    if not (request.session['user'][14] == '3' or request.session['user'][14] == '4'):
        return redirect('index')
    user_data = Member.objects.get(id = pk)
    if request.method == 'POST':
        if request.POST.get('how') == 'del':
            id = request.POST.get('id')
            Documents.objects.filter(id = id).delete()
            messages.info(request,'เรียบร้อย')
            return HttpResponseRedirect("/teacher/profile/documentsad/{}".format(pk))
        form = Documentform(request.POST,request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.teacher_id = user_data.id
            new.save()
            messages.info(request,'เรียบร้อย')
            return HttpResponseRedirect("/teacher/profile/documentsad/{}".format(pk))
    else:
        form = Documentform()
    doc_data = Documents.objects.filter(teacher_id = user_data.id)
    context = {'data':user_data,'doc_data':doc_data,'forms':form}
    return render(request,'teacher/documentsad.html',context)

def synctoSGS(request):
    if "user" not in request.session:
        return render(request,'login.html')
    user_data = Member.objects.get(id = request.session['user'][0])
    s_range = [x+1 for x in range(10)]
    context = {'s_range':s_range,'data':user_data}
    return render(request,'teacher/sgs.html',context)

def syncnow(request):
    if "user" not in request.session:
        return render(request,'login.html')
    if request.method == 'POST':
        serv = request.POST.get('server')
        username = request.POST.get('username')
        password = request.POST.get('password')
        browser = webdriver.Chrome(ChromeDriverManager().install())
        login = "https://sgs"+serv+".bopp-obec.info/sgs/Security/SignIn.aspx?MasterPage=../Master%20Pages/HorizontalMenu.master&Target="
        browser.get(login)
        username_input = browser.find_element_by_name("ctl00$PageContent$UserName")
        password_input = browser.find_element_by_name("ctl00$PageContent$Password")
        username_input.send_keys(username)
        password_input.send_keys(password+Keys.ENTER)
        link = "https://sgs%s.bopp-obec.info/sgs/TblTranscripts/Edit-TblTranscripts1-Table.aspx"%serv
        browser.get(link)
        time.sleep(10)
        return HttpResponseRedirect("/teacher/sgs")