from teacher.views import index
from PIL.Image import Image
from django.forms.models import ModelMultipleChoiceField
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse, FileResponse
from .models import Room, Studentdata,Checkname
from .forms import Checkform,Subjectform
from teacher.models import Subject
from project.models import Member
from django.db.models import Avg, Count, Min, Sum,Q, Max,CharField, Value
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse, FileResponse
from django.contrib import messages
import pandas as pd
import numpy as np
from pandas import DataFrame
from numpy import nan, s_
from PIL import Image
from bahttext import bahttext
import datetime

def Student(request):
    if "user" not in request.session:
        return render(request,'login.html')
    st_data = Studentdata.objects.all()
    if request.method == 'POST':
        file = request.FILES['fileup']
        dd = pd.read_csv(file)
        df = (dd.fillna(0)).replace(0.0,'None')
        r, c = df.shape
        header = ['id','st_id','title','fname','lname','nickname','sex','th_id','b_date','classroom','room','tel','email','status','address']
        for i in range(r):
            if str(df.iat[i,8]) == 'None':
                b_date = None
            else:
                b_date = datetime.date(str(df.iat[i,8]))
            st_data.create(
                st_id = int(df.iat[i,1]),
                title = str(df.iat[i,2]),
                fname = str(df.iat[i,3]),
                lname = str(df.iat[i,4]),
                nickname = str(df.iat[i,5]),
                sex = str(df.iat[i,6]),
                th_id = str(df.iat[i,7]),
                b_date = b_date,
                classroom = int(df.iat[i,9]),
                room = int(df.iat[i,10]),
                tel = str(df.iat[i,11]),
                email = str(df.iat[i,12]),
                status = str(df.iat[i,13]),
                address = str(df.iat[i,14])
            )
            
        return HttpResponseRedirect("/student/stdata/")

    else:
        df = None
    
    st_data = Studentdata.objects.all()
    context = {'st_data':st_data,'df':df}
    return render(request,'student/student.html',context)

def listroom(request):
    if "user" not in request.session:
        return render(request,'login.html')
    data = Member.objects.get(id = request.session["user"][0])
    s = Studentdata.objects.all()
    room = Room.objects.all()
    for i in room:
        count = s.filter(Q(classroom = i.classroom)&Q(room = i.room)).count()
        i.count = count
    context = {'data':data,'room':room}
    return render(request,'student/listroom.html',context)

def studentperroom(request,pk):
    if "user" not in request.session:
        return render(request,'login.html')
    room = Room.objects.get(id = pk)
    teacher_name = Member.objects.filter(Q(classroom = room.classroom)&Q(room = room.room)).values_list('fname','lname')
    st_data = Studentdata.objects.filter(Q(classroom = room.classroom)&Q(room = room.room))
    count_sex = list()
    count_sex.append(st_data.filter(sex = "ชาย").count())
    count_sex.append(st_data.filter(sex = "หญิง").count())
    context = {'st_data':st_data,'room':room,'teacher_name':teacher_name,'count_sex':count_sex}
    return render(request,'student/studentperroom.html',context)
        
def checkname(request):
    if "user" not in request.session:
        return render(request,'login.html')
    data = Member.objects.get(id = request.session["user"][0])
    s = Subject.objects.filter(teacher_id = data.id)
    if request.method == "POST":
        form = Subjectform(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.teacher_id = data.id
            new.save()
            messages.info(request,'เรียบร้อย')
            return HttpResponseRedirect("/student/checkname/")
    form = Subjectform()
    context = {'data':data,'s':s,'form':form}
    return render(request,'student/checkname.html',context)

def delcheck(request,pk,s):
    if "user" not in request.session:
        return render(request,'login.html')
    Checkname.objects.filter(id = pk).delete()
    messages.info(request,'เรียบร้อย')
    return HttpResponseRedirect("/student/checkname/dailycheck/{}".format(s))
    
def dailycheck(request,pk):
    if "user" not in request.session:
        return render(request,'login.html')
    data = Member.objects.get(id = request.session["user"][0])
    s_detail = Subject.objects.get(id = pk)
    student_name = Studentdata.objects.filter(Q(classroom = s_detail.classroom)&Q(room = s_detail.room))
    if request.method == "POST":
        date = request.POST.get("date")
        for i in student_name:
            ra = request.POST.get("check{}".format(i.id))
            if ra != "มา":
                Checkname.objects.create(
                    st_id = i.st_id,
                    sem = 1,
                    year = 2564,
                    subject = s_detail.subject_id,
                    date = date,
                    status = ra,
                    classroom = i.classroom,
                    room = i.room
                )
        messages.info(request,'เรียบร้อย')
        return HttpResponseRedirect("/student/checkname/dailycheck/{}".format(s_detail.id))
    listhistory = Checkname.objects.filter(Q(subject = s_detail.subject_id)&Q(room = s_detail.room)&Q(classroom = s_detail.classroom))
    for i in listhistory:
            sdata = student_name.get(st_id = i.st_id)
            fullname = sdata.title+sdata.fname+" "+sdata.lname
            i.fullname = fullname

    form = Checkform()
    context = {'data':data,'s':s_detail,'student_name':student_name,'listhistory':listhistory,'form':form}
    return render(request,'student/dailycheck.html',context)