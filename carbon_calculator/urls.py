from django.urls import path

from . import views

app_name = 'carbon_calculator'

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
#    path('', views.IndexView.as_view(), name='index'),
    path('eventcalculator', views.eventcalculator, name='eventcalculator'),
    path('stations', views.StationsView.as_view(), name='stations'),
    #path('stations', views.stations, name='stations'),
    path('stations/<int:pk>/', views.StationDetailView.as_view(), name='station-detail'),
    #path('stationdetail', views.stationdetail, name='stationdetail'),
    #path('', views.IndexView.as_view(), name='index'),
    #path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    #path('<int:question_id>/vote/', views.vote, name='vote'),
 ]