from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

admin.autodiscover()
urlpatterns = [
    path('stdata/',views.Student,name='stdata'),
    path('stdata/listroom',views.listroom,name='listroom'),
    path('stdata/listroom/room/<int:pk>',views.studentperroom,name='studentperroom'),
    path('checkname/',views.checkname,name='checkname'),
    path('checkname/dailycheck/<int:pk>',views.dailycheck,name='dailycheck'),
    path('checkname/delete/<int:pk>/<int:s>',views.delcheck,name='delcheck'),


]