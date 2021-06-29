from django.contrib import admin
from .models import Studentdata,Checkname
from teacher.models import Subject

# Register your models here.
admin.site.register(Studentdata)
admin.site.register(Subject)