from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

admin.autodiscover()
urlpatterns = [
    path('',views.index,name='index'),
    path('profile/',views.Profile,name='profile'),
    path('allteacher/',views.Allteacher,name='allteacher'),
    path('profile/documents',views.documents,name='documents'),
    path('profile/documentsad/<int:pk>',views.documentsAdmin,name='documentsad'),
    path('profilead/<int:pk>',views.ProfileAdmin,name='profilead'),
    path('sgs/',views.synctoSGS,name='sgs'),
    path('sgs/syncnow',views.syncnow,name='syncnow'),

]