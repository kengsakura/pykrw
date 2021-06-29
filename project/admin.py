from django.contrib import admin
from .models import Member,Baseschooldata,Majoractivity,Minoractivity,MinorObjective,MinorGoal,MinorOperation,MinorCost,MinorEvaluation,MinorBenefit,Usemoney,Numberofuse
class DesignMember(admin.ModelAdmin):
    list_display = ['id','fname','lname','status']
    list_per_page = 10
    list_filter = ['status']
    search_fields = ['fname','fname']
class DesignBase(admin.ModelAdmin):
    list_display = ['id','type_dta','order']
    list_per_page = 10
class DesignMajor(admin.ModelAdmin):
    list_display = ['id','name','responsible','money']
    list_per_page = 10
    list_filter = ['responsible']
    search_fields = ['name','responsible']
    list_editable = ['name','responsible','money']
class Normal(admin.ModelAdmin):
    list_display = ['id','minor_id','order','detail']
    list_per_page = 10

# Register your models here.
admin.site.register(Member,DesignMember)
admin.site.register(Majoractivity,DesignMajor)
admin.site.register(Minoractivity,DesignMajor)
admin.site.register(MinorObjective,Normal)
admin.site.register(MinorGoal,Normal)
admin.site.register(MinorOperation,Normal)
admin.site.register(MinorCost,Normal)
admin.site.register(MinorEvaluation,Normal)
admin.site.register(MinorBenefit,Normal)
admin.site.register(Baseschooldata)
admin.site.register(Numberofuse)
admin.site.register(Usemoney)