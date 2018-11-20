
from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.mainpage,name='home'),
    path('contact/',views.contact,name='contact'),
    path('contact/success/',views.successView,name='success'),
    path('timetable/',views.timetable,name='timetable'),
    path('timetable/search/', views.search,name='search'),
    path('forum/',views.temp,name='temp'),
    # url(r'^forum/match$',views.matchsuccess,name='match'),
    # url(r'^forum/nomatch$',views.nomatch,name='nomatch'),

   ]
