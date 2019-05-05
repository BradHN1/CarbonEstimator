from django.urls import path

from . import views

app_name = 'carbon_calculator'

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
#    path('', views.IndexView.as_view(), name='index'),
    path('eventcalculator', views.eventcalculator, name='eventcalculator'),
    path('stations', views.stations, name='stations'),
    path('stationdetail', views.stationdetail, name='stationdetail'),
 ]