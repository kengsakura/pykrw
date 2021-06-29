from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

admin.autodiscover()
urlpatterns = [
    path('',views.index,name='index'),
    path('offer/',views.Offer,name='offer'),
    path('minorlist/',views.Minorlist,name='minorlist'),
    path('checkminor/',views.Checkminor,name='checkminor'),
    path('checkminor/detailminor/<int:pk>/',views.Detailminor,name='detailminor'),
    path('checkminor/addform/<int:pk>/',views.Addform,name='addform'),
    path('checkminor/addform1/<int:pk>/',views.Addform1,name='addform1'),
    path('checkminor/addform2/<int:pk>/',views.Addform2,name='addform2'),
    path('checkminor/addform3/<int:pk>/',views.Addform3,name='addform3'),
    path('checkminor/addform4/<int:pk>/',views.Addform4,name='addform4'),
    path('checkminor/addform5/<int:pk>/',views.Addform5,name='addform5'),
    path('checkminor/addform6/<int:pk>/',views.Addform6,name='addform6'),
    path('checkminor/addform7/<int:pk>/',views.Addform7,name='addform7'),
    path('checkminor/generate/<int:pk>/',views.addpdf,name='addpdf'),
    path('manage/',views.Manage,name='manage'),
    path('uselist/',views.Uselist,name='uselist'),
    path('manage/confirm/',views.Confirm,name='confirm'),
    path('manage/confirm_2/<int:pk>/',views.Confirm_2,name='confirm_2'),
    path('delconfirm/<int:pk>/',views.Del_confirm,name='del_confirm'),
    path('checkminor/usemoney/<int:pk>/',views.Use_money,name='usemoney'),
    path('checkminor/usemoney/ask/<int:pk>/<int:no>/',views.Ask,name='ask'),
    path('export/', views.export_users_csv, name='export_users_csv'),
    path('checkminor/usemoney/ask/<int:nid>/',views.ask_pdf,name='ask_pdf'),
    path('manage/addclass/',views.addclass,name='addclass'),
    path('manage/addteacher/',views.addteacher,name='addteacher'),

]