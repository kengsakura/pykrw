from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse, FileResponse
from django.contrib import messages
from django.db.models import Avg, Count, Min, Sum,Q, Max,CharField, Value
from datetime import datetime, date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from textwrap import wrap
from reportlab.lib import pagesizes
from reportlab.lib import styles
import csv
from pythainlp import sent_tokenize, word_tokenize

from django.views.generic import ListView
from reportlab.platypus.doctemplate import SimpleDocTemplate
from .models import Member,Majoractivity,Minoractivity,MinorObjective,MinorIntroduction,MinorGoal,MinorOperation,MinorCost,MinorEvaluation,MinorBenefit,Usemoney,Numberofuse,Baseschooldata
from .forms import Basedata, Memberform,Majorform,Minorform,Objectiveform,Introform,Goalform,Operationform,Costform,Evaform,Benefitform,Usemoneyform,Numberofuseform,Roomform
from student.models import Room
from django.urls import reverse_lazy,reverse
from pythainlp.util import thai_strftime
from bahttext import bahttext
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter,A4,landscape
from reportlab.lib.units import mm,inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import magenta, red,CMYKColor,blueviolet,black
from reportlab.platypus import Paragraph, Table, TableStyle,SimpleDocTemplate,Frame,HRFlowable,PageBreak

#from werkzeug.wsgi import FileWrapper
from pathlib import Path
import io
import os
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
    allmoney_text = bahttext(allmoney)
    total_text = bahttext(currentuse)
    context = {'dashlist':dashlist,'allmoney':allmoney_text,'total':total_text}
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
    request.session.modified = True
    return render(request,'login.html')
def Offer(request):
    if "user" not in request.session:
        return render(request,'login.html')
    if request.method == "POST":
        name = request.session["user"][2]+" "+request.session["user"][3]
        form = Minorform(request.POST,{'responsible' : name})
        if form.is_valid():
            new_record = form.save(commit=False)
            new_record.responsible = name
            new_record.save()
            messages.info(request,"เรียบร้อย")
            return HttpResponseRedirect("/project/offer/")
        else:
            print(form.errors)
    else:
        form = Minorform()
    offerform = Minorform()
    data = Member.objects.get(Q(fname = request.session["user"][2])&Q(lname = request.session["user"][3]))
    context = {'form':offerform,'data':data}
    
    return render(request,'offer.html',context)

def Minorlist(request):
    if "user" not in request.session:
        return render(request,'login.html')
    minor = Minoractivity.objects.all()
    data = Member.objects.get(Q(fname = request.session["user"][2])&Q(lname = request.session["user"][3]))
    context = {'minors':minor,'data':data}
    return render(request,'minorlist.html',context)
def Checkminor(request):
    if "user" not in request.session:
        return render(request,'login.html')
    name = request.session["user"][2]+" "+request.session["user"][3]
    data_minor = Minoractivity.objects.filter(responsible=name)
    data = Member.objects.get(Q(fname = request.session["user"][2])&Q(lname = request.session["user"][3]))
    context = {'data':data,'data_minor':data_minor}
    return render(request,'check.html',context)
def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['id','major_id','year','date','name','responsible','branch','date_start','date_end','detail','money','ref1','ref2','ref3','cutoff','money_ask'])

    users = Minoractivity.objects.all().values_list('id','major_id','year','date','name','responsible','branch','date_start','date_end','detail','money','ref1','ref2','ref3','cutoff','money_ask')
    for user in users:
        writer.writerow(user)

    return response
def Detailminor(request,pk):
    if "user" not in request.session:
        return render(request,'login.html')
    data_minor = Minoractivity.objects.get(id=pk)
    data = Member.objects.get(Q(fname = request.session["user"][2])&Q(lname = request.session["user"][3]))
    form = Minorform(instance=data_minor)
    c1 = MinorIntroduction.objects.filter(minor_id = pk).count()
    c2 = MinorObjective.objects.filter(minor_id = pk).count()
    c3 = MinorGoal.objects.filter(minor_id = pk).count()
    c4 = MinorOperation.objects.filter(minor_id = pk).count()
    c5 = MinorCost.objects.filter(minor_id = pk).count()
    c6 = MinorEvaluation.objects.filter(minor_id = pk).count()
    c7 = MinorBenefit.objects.filter(minor_id = pk).count()
    c = [c1,c2,c3,c4,c5,c6,c7]
    context = {'data':data,'data_minor':data_minor,'form':form,'c':c}
    return render(request,'detail.html',context)

def Addform(request,pk):
    if "user" not in request.session:
        return render(request,'login.html')
    data_minor = Minoractivity.objects.get(id=pk)
    data = Member.objects.get(Q(fname = request.session["user"][2])&Q(lname = request.session["user"][3]))

    if request.method == "POST":
        form = Minorform(request.POST,instance=data_minor)
        if form.is_valid():
            form.save()
            messages.info(request,'บันทึกเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform/{}".format(pk))
    form = Minorform(instance=data_minor)
    context = {'form':form,'data':data,'data_minor':data_minor}
    return render(request,'addform.html',context)

def Addform1(request,pk):
    if "user" not in request.session:
        return render(request,'login.html')
    data_minor = Minoractivity.objects.get(id=pk)
    data = Member.objects.get(Q(fname = request.session["user"][2])&Q(lname = request.session["user"][3]))
    if request.method == "POST":
        if request.POST.get('how',' ') == 'edit':
            id_e = request.POST['id_e']
            order_e = request.POST['order_e']
            detail_e = request.POST['detail_e']
            ob = MinorIntroduction.objects.filter(id = id_e).update(
                order = order_e,
                detail = detail_e
            )
            messages.info(request,'แก้ไขเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform1/{}".format(pk))
        elif request.POST.get('how',' ') == 'del':
            id_e = request.POST['id_e']
            ob = MinorIntroduction.objects.get(id = id_e)
            ob.delete()
            messages.info(request,'ลบเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform1/{}".format(pk))
        form = Introform(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.minor_id = data_minor.id
            new.save()
            messages.info(request,'บันทึกเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform1/{}".format(pk))
    form = Introform()
    ob = MinorIntroduction.objects.filter(minor_id=pk)
    context = {'form':form,'data':data,'ob':ob,'data_minor':data_minor}
    return render(request,'addform1.html',context)

def Addform2(request,pk):
    if "user" not in request.session:
        return render(request,'login.html')
    data_minor = Minoractivity.objects.get(id=pk)
    if request.method == "POST":
        if request.POST.get('how',' ') == 'edit':
            id_e = request.POST['id_e']
            order_e = request.POST['order_e']
            detail_e = request.POST['detail_e']
            ob = MinorObjective.objects.filter(id = id_e).update(
                order = order_e,
                detail = detail_e
            )
            messages.info(request,'แก้ไขเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform2/{}".format(pk))
        elif request.POST.get('how',' ') == 'del':
            id_e = request.POST['id_e']
            ob = MinorObjective.objects.get(id = id_e)
            ob.delete()
            messages.info(request,'ลบเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform2/{}".format(pk))
        form = Objectiveform(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.minor_id = data_minor.id
            new.save()
            messages.info(request,'บันทึกเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform2/{}".format(pk))
    ob = MinorObjective.objects.filter(minor_id=pk)
    form = Objectiveform()
    context = {'form':form,'ob':ob,'data_minor':data_minor}
    return render(request,'addform2.html',context)

def Addform3(request,pk):
    if "user" not in request.session:
        return render(request,'login.html')
    data = Minoractivity.objects.get(id=pk)
    if request.method == "POST":
        if request.POST.get('how',' ') == 'edit':
            id_e = request.POST['id_e']
            type_e = request.POST['type_e']
            order_e = request.POST['order_e']
            detail_e = request.POST['detail_e']
            ob = MinorGoal.objects.filter(id = id_e).update(
                type_goal = type_e,
                order = order_e,
                detail = detail_e
            )
            messages.info(request,'แก้ไขเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform3/{}".format(pk))
        elif request.POST.get('how',' ') == 'del':
            id_e = request.POST['id_e']
            ob = MinorGoal.objects.get(id = id_e)
            ob.delete()
            messages.info(request,'ลบเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform3/{}".format(pk))
        form = Goalform(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.minor_id = data.id
            new.save()
            messages.info(request,'บันทึกเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform3/{}".format(pk))
    ob = MinorGoal.objects.filter(minor_id=pk)
    form = Goalform()
    context = {'form':form,'data':data,'ob':ob}
    return render(request,'addform3.html',context)

def Addform4(request,pk):
    if "user" not in request.session:
        return render(request,'login.html')
    data = Minoractivity.objects.get(id=pk)
    if request.method == "POST":
        if request.POST.get('how',' ') == 'edit':
            id_e = request.POST['id_e']
            type_e = request.POST['type_e']
            order_e = request.POST['order_e']
            detail_e = request.POST['detail_e']
            date_e = request.POST['date_e']
            responsible_e = request.POST['responsible_e']
            ob = MinorOperation.objects.filter(id = id_e).update(
                type_op = type_e,
                order = order_e,
                detail = detail_e,
                date = date_e,
                responsible = responsible_e
            )
            messages.info(request,'แก้ไขเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform4/{}".format(pk))
        elif request.POST.get('how',' ') == 'del':
            id_e = request.POST['id_e']
            ob = MinorOperation.objects.get(id = id_e)
            ob.delete()
            messages.info(request,'ลบเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform4/{}".format(pk))
        form = Operationform(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.minor_id = data.id
            new.save()
            messages.info(request,'บันทึกเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform4/{}".format(pk))
    ob = MinorOperation.objects.filter(minor_id=pk)
    form = Operationform()
    context = {'form':form,'data':data,'ob':ob}
    return render(request,'addform4.html',context)

def Addform5(request,pk):
    if "user" not in request.session:
        return render(request,'login.html')
    data = Minoractivity.objects.get(id=pk)
    if request.method == "POST":
        if request.POST.get('how',' ') == 'edit':
            id_e = request.POST['id_e']
            order_e = request.POST['order_e']
            detail_e = request.POST['detail_e']
            count_e = request.POST['count_e']
            unit_e = request.POST['unit_e']
            money_e = request.POST['money_e']
            ob = MinorCost.objects.filter(id = id_e).update(
                order = order_e,
                detail = detail_e,
                count = count_e,
                unit = unit_e,
                money = money_e,
                totalmoney = float(money_e)*float(count_e)
            )
            messages.info(request,'แก้ไขเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform5/{}".format(pk))
        elif request.POST.get('how',' ') == 'del':
            id_e = request.POST['id_e']
            ob = MinorCost.objects.get(id = id_e)
            ob.delete()
            messages.info(request,'ลบเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform5/{}".format(pk))
        form = Costform(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.minor_id = data.id
            new.totalmoney = float(new.count)*float(new.money)
            new.save()
            
            messages.info(request,'บันทึกเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform5/{}".format(pk))
    ob = MinorCost.objects.filter(minor_id=pk)
    form = Costform()
    if ob.first() == None:
        sum = 0
        
    else:
        sum = ob.aggregate(Sum('totalmoney'))['totalmoney__sum']
    Minoractivity.objects.filter(id=pk).update(
                money_ask = sum
            )
    context = {'form':form,'data':data,'ob':ob,'sum':sum,'bahttext':bahttext(sum)}
    return render(request,'addform5.html',context)

def Addform6(request,pk):
    if "user" not in request.session:
        return render(request,'login.html')
    data = Minoractivity.objects.get(id=pk)
    if request.method == "POST":
        if request.POST.get('how',' ') == 'edit':
            id_e = request.POST['id_e']
            type_e = request.POST['type_e']
            order_e = request.POST['order_e']
            detail_e = request.POST['detail_e']
            criteria_e = request.POST['criteria_e']
            method_e = request.POST['method_e']
            measure_e = request.POST['measure_e']
            ob = MinorEvaluation.objects.filter(id = id_e).update(
                type_ev = type_e,
                order = order_e,
                detail = detail_e,
                criteria = criteria_e,
                method = method_e,
                measure = measure_e
            )
            messages.info(request,'แก้ไขเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform6/{}".format(pk))
        elif request.POST.get('how',' ') == 'del':
            id_e = request.POST['id_e']
            ob = MinorEvaluation.objects.get(id = id_e)
            ob.delete()
            messages.info(request,'ลบเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform6/{}".format(pk))
        form = Evaform(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.minor_id = data.id
            new.save()
            messages.info(request,'บันทึกเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform6/{}".format(pk))
    ob = MinorEvaluation.objects.filter(minor_id=pk)
    form = Evaform()
    context = {'form':form,'data':data,'ob':ob}
    return render(request,'addform6.html',context)


def Addform7(request,pk):
    if "user" not in request.session:
        return render(request,'login.html')
    data = Minoractivity.objects.get(id=pk)
    if request.method == "POST":
        if request.POST.get('how',' ') == 'edit':
            id_e = request.POST['id_e']
            order_e = request.POST['order_e']
            detail_e = request.POST['detail_e']
            ob = MinorBenefit.objects.filter(id = id_e).update(
                order = order_e,
                detail = detail_e
            )
            messages.info(request,'แก้ไขเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform7/{}".format(pk))
        elif request.POST.get('how',' ') == 'del':
            id_e = request.POST['id_e']
            ob = MinorBenefit.objects.get(id = id_e)
            ob.delete()
            messages.info(request,'ลบเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform7/{}".format(pk))
        form = Benefitform(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.minor_id = data.id
            new.save()
            messages.info(request,'บันทึกเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/addform7/{}".format(pk))
    ob = MinorBenefit.objects.filter(minor_id=pk)
    form = Benefitform()
    context = {'form':form,'data':data,'ob':ob}
    return render(request,'addform7.html',context)



def Use_money(request,pk):
    if "user" not in request.session:
        return render(request,'login.html')
    data = Minoractivity.objects.get(id=pk)
    form = Numberofuseform()
    if request.method == "POST":
        if request.POST.get('how') == 'del':
            n_id = request.POST.get('askid')
            before = Numberofuse.objects.filter(id = n_id)
            wait = Usemoney.objects.filter(Q(minor_id = (before.first()).minor_id)&Q(no =(before.first()).no )).delete()
            before.delete()
            messages.info(request,'ลบเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/usemoney/{}".format(data.id))
        form = Numberofuseform(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.minor_id = pk
            new.save()
            messages.info(request,'เรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/usemoney/{}".format(data.id))
    #use = Usemoney.objects.filter(minor_id=pk).values_list('no')
    #print(use)
    number = Numberofuse.objects.filter(minor_id = pk)
    if number.aggregate(Sum('money'))['money__sum'] == None:
        currentuse = 0
    else:
        currentuse = number.aggregate(Sum('money'))['money__sum']
    balance = data.money - currentuse
    context = {'data':data,'form':form,'number':number,'current':currentuse,'bal':balance}
    return render(request,'usemoney.html',context)

def Confirm(request):
    if "user" not in request.session:
        return render(request,'login.html')
    data = Minoractivity.objects.all()
    usedata = Usemoney.objects.all()
    numberofuse_c = Numberofuse.objects.filter(status = '1').order_by('-date')
    numberofuse_nc = Numberofuse.objects.filter(status = '0').order_by('-date')
    for i in numberofuse_c:
        minor_name = data.get(id = i.minor_id).name
        minor_res = data.get(id = i.minor_id).responsible
        i.new_name = minor_name # This line is the problem
        i.res = minor_res
    for i in numberofuse_nc:
        minor_name = data.get(id = i.minor_id).name
        minor_res = data.get(id = i.minor_id).responsible
        i.new_name = minor_name # This line is the problem
        i.res = minor_res
    context = {'data':data,'usedata':usedata,'c':numberofuse_c,'nc':numberofuse_nc}
    return render(request,'confirm.html',context)

def Confirm_2(request,pk):
    if "user" not in request.session:
        return render(request,'login.html')
    data = Minoractivity.objects.all()
    numberofuse = Numberofuse.objects.get(id = pk)
    usedata = Usemoney.objects.filter(Q(minor_id = numberofuse.minor_id)&Q(no = numberofuse.no))
    if request.method == 'POST':
        id = request.POST.get('id')
        Numberofuse.objects.filter(id = id).update(
            status = 1
        )
        messages.info(request,'เรียบร้อย')
        return HttpResponseRedirect("/project/manage/confirm/")
    context = {'data':data,'usedata':usedata,'numberofuse':numberofuse}
    return render(request,'confirm_2.html',context)

def Manage(request):
    if "user" not in request.session:
        return render(request,'login.html')
    if not (request.session['user'][14] == '3' or request.session['user'][14] == '2'):
        return redirect('index')
    context = {}
    return render(request,'manage.html',context)

def Ask(request,pk,no):
    if "user" not in request.session:
        return render(request,'login.html')
    data = Minoractivity.objects.get(id=pk)
    n = Numberofuse.objects.filter(Q(minor_id=pk)&Q(no=no))
    number = n.first()
    if request.method == 'POST':
        if request.POST.get('how') == 'edit':
            ask_id = request.POST.get('askid')
            detail_e = request.POST.get('detail_e')
            count_e = request.POST.get('count_e')
            unit_e = request.POST.get('unit_e')
            money_e = request.POST.get('money_e')
            Usemoney.objects.filter(id = ask_id).update(
                detail = detail_e,
                count = count_e,
                unit = unit_e,
                money = money_e,
                total = (float(count_e)*float(money_e))
            )
            n.update(
                money = (Usemoney.objects.filter(Q(minor_id=pk)&Q(no=no)).aggregate(Sum('total'))['total__sum'])
            )
            messages.info(request,'แก้ไขเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/usemoney/ask/{}/{}".format(pk,no))
        if request.POST.get('how') == 'del':
            ask_id = request.POST.get('askid')
            total_e = request.POST.get('total_e')
            Usemoney.objects.filter(id = ask_id).delete()
            n.update(
                money = (float(number.money) - float(total_e))
            )
            messages.info(request,'ลบเรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/usemoney/ask/{}/{}".format(pk,no))
        form = Usemoneyform(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.minor_id = data.id
            new.no = number.no
            new.date = number.date
            new.total = new.money * new.count
            new.save()
            if number.money == None:
                total = new.total
            else:
                total = number.money + new.total
            Numberofuse.objects.filter(Q(minor_id=pk)&Q(no=no)).update(
                money = total
            )
            messages.info(request,'เรียบร้อย')
            return HttpResponseRedirect("/project/checkminor/usemoney/ask/{}/{}".format(data.id,number.no))
    form = Usemoneyform()
    if n.aggregate(Sum('money'))['money__sum'] == None:
        currentuse = 0
    else:
        currentuse = n.aggregate(Sum('money'))['money__sum']
    if Numberofuse.objects.filter(minor_id = pk).aggregate(Sum('money'))['money__sum'] == None:
        all_use = 0
    else:        
        all_use = Numberofuse.objects.filter(minor_id = pk).aggregate(Sum('money'))['money__sum']
    balance = data.money - all_use
    askdata = Usemoney.objects.filter(Q(minor_id=pk)&Q(no=no))
    context = {'form':form,'data':data,'number':number,'ask':askdata,'bal':balance,'current':currentuse}
    return render(request,'ask.html',context)
def addclass(request):
    if "user" not in request.session:
        return render(request,'login.html')
    if request.session["user"][14] != '3':
        return redirect('index')
    if request.method == "POST":
        form = Roomform(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,'เรียบร้อย')
            return HttpResponseRedirect("/project/manage/addclass/")
    form = Roomform()
    room = Room.objects.all()
    context = {'form':form,'room':room}
    return render(request,'addclass.html',context)
def addteacher(request):
    if "user" not in request.session:
        return render(request,'login.html')
    if request.session["user"][14] != '3':
        return redirect('index')
    if request.method == "POST":
        classroom = request.POST.getlist('classroom')
        croom = request.POST.getlist('room')
        t_id = request.POST.getlist('t_id')
        for i in range(len(t_id)):
            if croom[i] =="" or classroom[i] == "":
                continue
            Member.objects.filter(id = t_id[i]).update(
                classroom = classroom[i],
                room = croom[i],
            )
        messages.info(request,'เรียบร้อย')
        return HttpResponseRedirect("/project/manage/addteacher/")
    data = Member.objects.all()
    sroom = Room.objects.all()
    for i in sroom:
        teacher_name = data.filter(Q(classroom = i.classroom)&Q(room = i.room)).values_list('fname','lname')
        i.teacher_name = teacher_name
    context = {'data':data,'room':sroom}
    return render(request,'addteacherclass.html',context)
    
def Uselist(request):
    if "user" not in request.session:
        return render(request,'login.html')
    data = Minoractivity.objects.all()
    usedata = Usemoney.objects.all()
    numberofuse = Numberofuse.objects.all()
    for i in numberofuse:
        minor_name = data.get(id = i.minor_id).name
        minor_res = data.get(id = i.minor_id).responsible
        sub= usedata.filter(Q(minor_id=i.minor_id)&Q(no=i.no)).values_list('detail','money','count','total')
        i.new_name = minor_name # This line is the problem
        i.res = minor_res
        i.subact = sub    
    
    context = {'data':data,'usedata':usedata,'c':numberofuse}
    return render(request,'uselist.html',context)

def Del_confirm(request,pk):
    if "user" not in request.session:
        return render(request,'login.html')
    Numberofuse.objects.filter(id=pk).delete()
    messages.info(request,'ลบเรียบร้อย')
    return HttpResponseRedirect("/project/manage/confirm/")
#BACKUP
def ask_pdf(request,nid):
    if "user" not in request.session:
        return render(request,'login.html')
    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
    pdfmetrics.registerFont(TTFont('reg', os.path.join(BASE_DIR,'static','font','THSarabunNew.ttf')))
    pdfmetrics.registerFont(TTFont('bold', os.path.join(BASE_DIR,'static','font','THSarabunNew Bold.ttf')))
    pdfmetrics.registerFont(TTFont('ita', os.path.join(BASE_DIR,'static','font','THSarabunNew Italic.ttf')))
    pdfmetrics.registerFont(TTFont('bi', os.path.join(BASE_DIR,'static','font','THSarabunNew BoldItalic.ttf')))
    pdfmetrics.registerFont(TTFont('threg', os.path.join(BASE_DIR,'static','font','THSarabunIT๙.ttf')))
    pdfmetrics.registerFont(TTFont('thbold', os.path.join(BASE_DIR,'static','font','THSarabunIT๙ Bold.ttf')))
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer,pagesize=A4)
    numberofuse = Numberofuse.objects.get(id=nid)
    data = Minoractivity.objects.get(id = numberofuse.minor_id)
    myname = (data.responsible).strip().split(' ')
    member = Member.objects.get(Q(fname=myname[0])&Q(lname=myname[1]))
    alluse = Numberofuse.objects.filter(minor_id = data.id)
    use_data = Usemoney.objects.filter(Q(minor_id = numberofuse.minor_id)&Q(no = numberofuse.no))
    base_year = Baseschooldata.objects.get(type_dta = 'ปีการศึกษา')
    
    fullname = member.title+member.fname+"  "+member.lname
    #fullname = request.session["user"][1]+request.session["user"][2]+"&nbsp;&nbsp;"+request.session["user"][3]
    currentmoney = data.money
    major = Majoractivity.objects.get(id = data.major_id)
    if alluse:
        for i in alluse:
            if i.no < numberofuse.no:
                currentmoney = currentmoney-(i.money)
    ask_use = numberofuse.money
    try:
        balance = currentmoney-ask_use
    except:
        print("An exception occurred")
    
    #content
    p.setFont('bold',24)
    if not use_data:
        p.drawCentredString(105*mm,269*mm,'ยังไม่มีข้อมูล') #header
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, filename='ask_{}.pdf'.format(nid),content_type='application/pdf')
    p.drawCentredString(105*mm,269*mm,'บันทึกข้อความ') #header
    p.drawImage(os.path.join(BASE_DIR,'static','images','symbol.png'),20*mm,267*mm,15*mm,15*mm, mask='auto')
    f = Frame(20*mm,15*mm,170*mm,255*mm,showBoundary=0)
    story = []
    styles = getSampleStyleSheet()
    style_n = styles['Normal']
    body = ParagraphStyle('yourtitle',
                           fontName="threg",
                           fontSize=16,
                           parent=styles['Heading2'],
                           alignment=0,
                           leading=20,
                           )
    story.append(Paragraph("<para fontname = 'threg' size = '16' leading = '20'><font fontname = 'thbold' size = '18'>ส่วนราชการ  </font> &nbsp;&nbsp;โรงเรียนการุ้งวิทยาคม อำเภอบ้านไร่ จังหวัดอุทัยธานี 61180</para>"))
    story.append(Paragraph("<para fontname = 'threg' size = '16' leading = '20'><font fontname = 'thbold' size = '18'>ที่  </font> &nbsp;&nbsp;ศธ. 04350.02/................................<font fontname = 'bold' size = '18'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;วันที่  &nbsp;&nbsp;</font>"+str(thai_strftime(numberofuse.date,"%d %B %Y"))+"</para>"))
    story.append(Paragraph("<para fontname = 'threg' size = '16' leading = '22'><font fontname = 'thbold' size = '18'>เรื่อง  </font> &nbsp;&nbsp;ขออนุมัติงบประมาณดำเนินการตามกิจกรรมในแผนปฏิบัติการประจำปีการศึกษา {}</para>".format(base_year.value)))
    story.append(HRFlowable(width='100%', spaceBefore = 2,thickness=0.5, color=colors.black))
    story.append(Paragraph("<para fontname = 'threg' size = '16' spaceBefore='6' leading = '22'><font fontname = 'thbold' >เรียน</font>&nbsp;&nbsp;&nbsp; ผู้อำนวยการโรงเรียนการุ้งวิทยาคม </para>"))
    story.append(Paragraph("<para fontname = 'threg' firstLineIndent = '37' size = '16' leading = '20' >ตามที่โรงเรียนการุ้งวิทยาคมได้มอบหมาย กลุ่มงาน{} เป็นผู้รับผิดชอบ งาน/โครงการ {} ชื่อกิจกรรม {} ซึ่งได้รับการจัดสรรงบประมาณ จำนวน {:,} บาท</para>".format(data.branch,major.name,data.name,data.money)))
    story.append(Paragraph("<para fontname = 'threg' firstLineIndent = '37' size = '16' leading = '20' >เพื่อให้การปฏิบัติงานดังกล่าวเป็นไปตามระยะเวลา และสอดคล้องกับกิจกรรมที่กำหนดไว้ในแผนฯ จึงขออนุมัติการดำเนินงานตามโครงการและอนุมัติใช้เงิน{} จำนวน {:,} บาท</para>".format(numberofuse.type_money,ask_use)))
    story.append(Paragraph("<para fontname = 'threg' spaceBefore='6'firstLineIndent = '37' size = '16' leading = '20' >จึงเรียนมาเพื่อโปรดพิจารณา</para>"))
    para_sign = Paragraph("<para fontname = 'threg'ALIGN = 'center' size = '16' leading = '20' spaceAfter='6'>ลงชื่อ"+'&nbsp;'*39+"<br/>\n({})<br/>\nผู้รับผิดชอบ</para>".format(fullname))
    sign = [['',para_sign]]
    t0 = Table(sign,[50*mm,110*mm],style = [
    ('ALIGN',(0,0),(0,-1),'LEFT'),
    ('VALIGN',(0,0),(0,-1),'TOP')])

    detail_1 = Paragraph("<para fontname = 'threg'size = '16' leading = '18'><font face = 'thbold'><u>1. ความเห็นงานแผนงาน</u></font><br/>\n\
        <font size = '16'>ตามแผนปฏิบัติการประจำปี</font><br/>\n<font size = '16'>&nbsp;&nbsp;(&nbsp;&nbsp;) มีในแผน/ทำตามแผน</font>\
        <br/>\n<font size = '16'>&nbsp;&nbsp;(&nbsp;&nbsp;) ไม่มีในแผน</font></para>")
    detail_2 = Paragraph("<para fontname = 'threg'size = '16' leading = '18'><font face = 'thbold'><u>2. ความเห็นหัวหน้าเจ้าหน้าที่พัสดุ</u></font><br/>\n\
        <font size = '16'>ได้ตรวจสอบรายการจัดซื้อ/จ้าง แล้ว</font><br/>\n<font size = '16'>&nbsp;&nbsp;(&nbsp;&nbsp;) ตรงตามวัตถุประสงค์ สมควรดำเนินการได้</font>\
        <br/>\n<font size = '16'>&nbsp;&nbsp;(&nbsp;&nbsp;) ไม่ตรงตามวัตถุประสงค์</font><br/>\n\
        </para>")
    detail_3 = Paragraph("<para fontname = 'threg'size = '16' leading = '18'><font face = 'thbold'><u>3. ความเห็นเจ้าหน้าที่การเงิน</u></font><br/>\n\
        <font size = '16'>งาน/โครงการได้รับอนุมัติและเบิกจ่าย</font><br/>\n<font size = '16'>จำนวนเงิน.................................บาท เรียบร้อยแล้ว</font></para>")
    detail_4 = Paragraph("<para fontname = 'threg'size = '16' leading = '18'><font face = 'thbold'><u>4. ความเห็นรองผู้อำนวยการ</u></font><br/>\n\
        <font size = '16'>&nbsp;&nbsp;(&nbsp;&nbsp;) เห็นสมควรดำเนินการ</font>\
        <br/>\n<font size = '16'>&nbsp;&nbsp;(&nbsp;&nbsp;) ไม่สมควรดำเนินการ เพราะ............................</font><br/>\n\
        </para>")
    detailadd_1 = Paragraph("<para fontname = 'threg'size = '16' leading = '18' align = 'center'>ลงชื่อ"+'&nbsp;'*39+"<br/>\n(นางฉัตราภรณ์&nbsp;&nbsp;ว่องธัญกิจ)<br/>\n................/................/................</para>")
    detailadd_2 = Paragraph("<para fontname = 'threg'size = '16' leading = '18' align = 'center'>ลงชื่อ"+'&nbsp;'*39+"<br/>\n(นางสมคิด&nbsp;&nbsp;แป้นห้วย)<br/>\n................/................/................</para>")
    detailadd_3 = Paragraph("<para fontname = 'threg'size = '16' leading = '18' align = 'center'>ลงชื่อ"+'&nbsp;'*39+"<br/>\n(นางสาวปุริมปรัชญ์&nbsp;&nbsp;พันธ์เขียน)<br/>\n................/................/................</para>")
    detailadd_4 = Paragraph("<para fontname = 'threg'size = '16' leading = '18' align = 'center'>ลงชื่อ"+'&nbsp;'*39+"<br/>\n(นางสาววันวิสา&nbsp;&nbsp;วิเชียรรัตน์)<br/>\n................/................/................</para>")
    add_right = Paragraph("<para fontname = 'threg' align = 'right' size = '11' leading = '18'>ก่อนขอ {:,} บาท<br/>\nขอ {:,} บาท<br/>\nคงเหลือ {:,} บาท</para>".format(currentmoney,ask_use,balance))
    direct_comment = Paragraph("<para fontname = 'threg'align = 'center' size = '16' leading = '18'><font fontname = 'thbold' ><u>ความเห็นผู้อำนวยการโรงเรียน</u></font><br/>\n</para><para  fontname = 'threg' size = '16' leading = '18'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(&nbsp;&nbsp;) อนุมัติ"\
    +"&nbsp;"*66+"<br/>\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(&nbsp;&nbsp;) ไม่อนุมัติ เพราะ........................................................................<br/>\nลงชื่อ"+'&nbsp;'*40+"<br/>\n(นายถวัลย์&nbsp;&nbsp;วงษ์สาธุภาพ)<br/>\n................/................/................</para>")
    
    table_data = [[detail_1,add_right,detail_2],[detailadd_1,'',detailadd_2],[detail_3,'',detail_4],[detailadd_3,'',detailadd_4],[direct_comment,'','']]
    t1 = Table(table_data,[45*mm,40*mm,85*mm])
    t1.setStyle(TableStyle([('FONTNAME',(0,0),(0,-1),'bold'),
    #('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ('LINEBELOW',(0,1),(-1,1),0.25,colors.black),
    ('LINEABOVE',(0,-1),(-1,-1),0.25,colors.black),
    ('LINEAFTER',(1,0),(1,-2),0.25,colors.black),
    ('SIZE',(0,0),(-1,-1),16),('FONTNAME',(1,0),(1,-1),'reg'),
    ('LEADING',(0,1), (-1,-1),18),
    ('ALIGN',(0,0),(0,-1),'LEFT'),
    ('VALIGN',(0,0),(0,-1),'TOP'),
    #('SPAN',(0,0),(1,0)),
    ('SPAN',(0,1),(1,1)),
    ('SPAN',(0,2),(1,2)),
    ('SPAN',(0,3),(1,3)),
    ('SPAN',(0,-1),(-1,-1))]))
    story.append(t0)
    story.append(t1)

    f.addFromList(story,p)
    p.showPage()
    #doc = SimpleDocTemplate('mydoc.pdf',pagesize = A4)
    f2 = Frame(20*mm,20*mm,170*mm,249*mm,showBoundary=0)
    p.setFont('bold',18)
    p.drawCentredString(105*mm,275*mm,'รายละเอียดแนบท้ายการขออนุมัติใช้เงินงบประมาณ') #header
    story2=[]
    table_head = ['ที่','รายการ','จำนวน','ราคาต่อหน่วย','รวม']

    table_sum = [['รวม {:,} บาท'.format(numberofuse.money)],['({})'.format(bahttext(numberofuse.money))]]
    table_list = [table_head]
    n = 0
    for j in use_data:
        a = []
        n = n+1
        a.append(n)
        a.append(Paragraph(j.detail,body))
        a.append(Paragraph('{} {}'.format(j.count,j.unit),body))
        a.append('{:,}'.format(j.money))
        a.append('{:,}'.format(j.total))
        table_list.append(a)
    mystyle = [('FONTNAME',(0,0),(-1,-1),'threg'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ('SIZE',(0,0),(-1,-1),16),
    ('LEADING',(0,0), (-1,-1),20),
    ('FONTNAME',(0,0),(-1,0),'thbold'),
    ('ALIGN',(0,0),(-1,0),'CENTER'),
    ('ALIGN',(3,1),(3,-1),'RIGHT'),
    ('ALIGN',(4,1),(4,-1),'RIGHT'),
    ('ALIGN',(2,0),(2,-1),'CENTER'),
    ('ALIGN',(0,0),(0,-1),'CENTER'),
    ('VALIGN',(0,0),(0,-1),'MIDDLE'),
    ('VALIGN',(0,1),(-1,-1),'TOP')]
    sumstyle = [('FONTNAME',(0,0),(-1,-1),'thbold'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ('ALIGN',(0,0), (-1,-1),'RIGHT'),
    ('LEADING',(0,0), (-1,-1),20),
    ('SIZE',(0,0),(-1,-1),16),
    ]
    cons = 28.34645669
    t2 = Table(table_list,[10*mm,75*mm,25*mm,30*mm,30*mm])
    t2.setStyle(TableStyle(mystyle))
    t_sum = Table(table_sum,[170*mm])
    t_sum.setStyle(TableStyle(sumstyle))
    table_height = t2.wrap(0, 100*mm)[1]
    print(table_height)
    if table_height>600:
        prenum = 26
        f_table = Table(table_list[:prenum],[10*mm,75*mm,25*mm,30*mm,30*mm])
        while f_table.wrap(0, 510)[1]>600:
            prenum = prenum - 1
            f_table = Table(table_list[:prenum],[10*mm,75*mm,25*mm,30*mm,30*mm])
        table_head = ['ที่','รายการ','จำนวน','ราคาต่อหน่วย','รวม']
        newhead = table_list[prenum:].copy()
        newhead.insert(0,table_head)
        l_table = Table(newhead,[10*mm,75*mm,25*mm,30*mm,30*mm])
        f_table.setStyle(TableStyle(mystyle))
        l_table.setStyle(TableStyle(mystyle))
        print(f_table.wrap(0, 100*mm)[1])
        print(l_table.wrap(0, 100*mm)[1])
        story2.append(f_table)
        f2.addFromList(story2,p)
        p.showPage()
        f3 = Frame(20*mm,20*mm,170*mm,249*mm,showBoundary=0)
        story3 = []
        story3.append(l_table)
        story3.append(t_sum)
        f3.addFromList(story3,p)
        p.showPage()
    else:
        story2.append(t2)
        story2.append(t_sum)
        f2.addFromList(story2,p)
        p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, filename='ask_{}.pdf'.format(nid),content_type='application/pdf')
def addpdf(request,pk):
    if "user" not in request.session:
        return render(request,'login.html')
    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
    #BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdfmetrics.registerFont(TTFont('reg', os.path.join(BASE_DIR,'static','font','THSarabunNew.ttf')))
    pdfmetrics.registerFont(TTFont('bold', os.path.join(BASE_DIR,'static','font','THSarabunNew Bold.ttf')))
    pdfmetrics.registerFont(TTFont('ita', os.path.join(BASE_DIR,'static','font','THSarabunNew Italic.ttf')))
    pdfmetrics.registerFont(TTFont('bi', os.path.join(BASE_DIR,'static','font','THSarabunNew BoldItalic.ttf')))
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer,pagesize=A4)
    p.setFont('bold',18)
    p.drawCentredString(105*mm,271*mm,'เสนอขอใช้เงินจัดกิจกรรม / งาน ปีการศึกษา 2564')
    p.setFont('reg', 16)
    story = []
    styles = getSampleStyleSheet()
    style_n = styles['Normal']
    header = ParagraphStyle('yourtitle',
                           fontName="bold",
                           fontSize=16,
                           parent=styles['Heading2'],
                           alignment=0,
                           leading=8,
                           spaceAfter=14)
    reg = ParagraphStyle('bodycontent',
                           fontName="reg",
                           firstLineIndent = 24,
                           fontSize=16,
                           parent=styles['Normal'],
                           alignment=4,
                           leading=20,
                           spaceAfter=8,
                           splitLongWords = 10,
                           justifyBreaks = 15,
                           wordWrap='CJK')
    data = Minoractivity.objects.get(id = pk)
    start_date = thai_strftime(data.date_start,"%d %b %Y")
    end_date = thai_strftime(data.date_end,"%d %b %Y")    
    f = Frame(25.4*mm,25.4*mm,159.2*mm,246.2*mm,showBoundary=0)
    headtable = [['ชื่องาน/กิจกรรม',Paragraph("<para fontname = 'reg' size='16' leading = '20' wordWrap='CJK'>"+data.name+"</para>")],['สนองกลยุทธ์ สพฐ.',data.ref1],['สนองกลยุทธ์สถานศึกษา',data.ref2],['สอดคล้องกับมาตรฐานการศึกษา (สพฐ.)',data.ref3],['ฝ่าย/งานที่รับผิดชอบ',data.branch],['ผู้รับผิดชอบโครงการ',data.responsible],
    ['ระยะเวลาดำเนินการ','{} ถึง {}'.format(start_date,end_date)],['งบประมาณที่ได้รับการจัดสรร',data.money],['งบประมาณที่ใช้ในการดำเนินงานครั้งนี้',data.money],['ลักษณะงาน/กิจกรรม',data.detail]]
    t0 = Table(headtable,[70*mm,80*mm],spaceAfter=15)
    t0.setStyle(TableStyle([('FONTNAME',(0,0),(0,-1),'bold'),
    ('SIZE',(0,0),(-1,-1),16),('FONTNAME',(1,0),(1,-1),'reg'),
    ('LEADING',(0,1), (-1,-1),18),
    ('ALIGN',(0,0),(0,-1),'LEFT'),
    ('VALIGN',(0,0),(0,-1),'TOP')]))
    #p = Paragraph("<font fontname = 'bold' size = '18'>เสนอขอใช้เงินจัดกิจกรรม / งาน ปีการศึกษา 2564</font>")
    #elems.append(p)
    story.append(t0)
    intro = Paragraph("1. หลักการและเหตุผล",header)
    story.append(intro)
    count_intro = MinorIntroduction.objects.filter(minor_id=pk).count()
    data_intro = MinorIntroduction.objects.filter(minor_id=pk)
    data_obj = MinorObjective.objects.filter(minor_id=pk)
    if data_intro:
        for i in data_intro:
            wraped_text = str(i.detail).replace('\n','<br />\n')
            #"<br/>".join(wrap(i.detail,159*mm))
            #text1 = word_tokenize(i.detail)
            story.append(Paragraph(wraped_text,reg))
    obj = Paragraph("2. วัตถุประสงค์",header)
    story.append(obj)
    if data_obj:
        for i in data_obj:
            #"<br/>".join(wrap(i.detail,159*mm))
            #text1 = word_tokenize(i.detail)
            story.append(Paragraph(str(i.order)+". "+i.detail,reg))
    datat= [['ที่', 'รายการ', 'ราคาต่อหน่วย', 'จำนวน', 'หน่วย'],
        ['00', '01', '02', '03', '04'],
    ['10', '11', '12', '13', '14'],
    ['20', '21', '22', '23', '24'],
    ['30', '31', '32', '33','20..............................................................']]
    t = Table(datat)
    t.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'bold'),
    ('SIZE',(0,0),(-1,-1),16),
    ('BOTTOMPADDING',(0,0),(-1,-1),10),
    ('FONTNAME',(0,1),(-1,-1),'reg'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ('LINEABOVE',(2,1),(2,-2),1,colors.pink),
    
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),]))
    story.append(t)
    f.addFromList(story,p)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, filename='minorac_{}.pdf'.format(pk),content_type='application/pdf')
    '''
    data = Minoractivity.objects.filter(id=pk).first()
    p = canvas.Canvas(buffer,pagesize=A4)
    p.setFont('bold',18)
    p.drawString(100, 100,data.name)
    styles = getSampleStyleSheet()
    style_n = styles['Normal']
    style_h = styles['Heading1']
    story = []
    datat= [['ที่', 'รายการ', 'ราคาต่อหน่วย', 'จำนวน', 'หน่วย'],
    ['00', '01', '02', '03', '04'],
 ['10', '11', '12', '13', '14'],
 ['20', '21', '22', '23', '24'],
 ['30', '31', '32', '33', '34']]
    t=Table(datat)
    story.append(Paragraph("Example",style_h))
    story.append(Paragraph("Hello every one",style_n))
    f = Frame(inch,inch,6*inch,9*inch,showBoundary=1)
    f.addFromList(story,p)

    #datat= [['ที่', 'รายการ', 'ราคาต่อหน่วย', 'จำนวน', 'หน่วย'],]
    datat= [['ที่', 'รายการ', 'ราคาต่อหน่วย', 'จำนวน', 'หน่วย'],
    ['00', '01', '02', '03', '04'],
 ['10', '11', '12', '13', '14'],
 ['20', '21', '22', '23', '24'],
 ['30', '31', '32', '33', '34']]
    #t=Table(datat)
    t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('SIZE',(0,0),(-1,-1),20),
    ('FONTNAME',(0,0),(-1,0),'bold'),
    ('FONTNAME',(0,1),(-1,-1),'reg'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))

    #t = Table(data)
    #t.setStyle(TableStyle([('FONT','bold')]))
    x,y=A4
    t.wrapOn(p,x,y)
    t.drawOn(p,100,100)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, filename='minorac_{}.pdf'.format(pk),content_type='application/pdf')'''
