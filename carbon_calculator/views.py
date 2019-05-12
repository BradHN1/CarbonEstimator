from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.db import models
from django.views import generic
from .estimator import Estimator
import datetime
import calendar

from pprint import pprint

#from django.views import generic
import logging

from .forms import NameForm, ContactForm, ExampleForm,StationDetailForm
from .models import Event, Attendee, Organizer, Sponsor, Station, Question, Community

event_name = 'Cooler Communities Event Calculator'
stationList = []
next_station = 1
estimator = Estimator()

# Create your views here.
def index(request):
    global event_name  
    event_name = estimator.GetEventName()
   
    # see if event is in database, if not, add it
    event = Event.objects.filter(name=event_name)
    if len(event)==0:

        datestring = estimator.GetEventDate()
        year = int(datestring[-4:])
        month = list(calendar.month_abbr).index(datestring[0:3])
        day = int(datestring[4:6])
        date = datetime.datetime(year, month, day)


        location= estimator.GetEventLocation()

        # add organizer if missing
        organizer_name = estimator.GetEventOrganizer()
        organizer = Organizer.objects.filter(name=organizer_name)
        if len(organizer)==0:
            organizer= Organizer(name=organizer_name)
            organizer.save()
        else:
            organizer = organizer.get(name=organizer_name)
        # add sponsor if missing
        sponsor_name = estimator.GetEventSponsor()
        sponsor = Sponsor.objects.filter(name=sponsor_name)
        if len(sponsor)==0:
            sponsor= Sponsor(name=sponsor_name)
            sponsor.save()
        else:
            sponsor = sponsor.get(name=sponsor_name)

        event = Event(name=event_name, date=date, location=location,organizer=organizer,sponsor=sponsor)
        event.save()
    
    welcome_context = {'EVENT_NAME':event_name}
    return render(request, 'carbon_calculator/welcome.html', welcome_context)
 
def about(request):
    global event_name
    event_name = estimator.GetEventName()
    about_context = {'EVENT_NAME':event_name}
    return render(request, 'carbon_calculator/about.html',about_context)

def eventcalculator(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            community = form.cleaned_data['community']
            phone = form.cleaned_data['phone']
            old_enough = form.cleaned_data['old_enough']

            matchingCommunities = Community.objects.filter(name=community)
            if len(matchingCommunities)==0:
                community = Community(name = community)
            else:
                community = matchingCommunities.get()

            if (old_enough[0]!='Y') and (old_enough[0]!='y'):
                age_acknowledgement=False
                firstName = "Underage"
                lastName = "Person"
                email = ""
                address = ""
                phone = ""
            else:
                age_acknowledgement=True
                attendee = Attendee.objects.filter(email=email)

            event = Event.objects.all()
            event_name = estimator.GetEventName()
            if len(event)>0:
                event = event.get(name=event_name)

            if lastName=="Person" or len(attendee)==0:
                attendee = Attendee(firstName=firstName, lastName=lastName, email=email,address=address,community=community,
                    phone=phone,age_acknowledgment=age_acknowledgement,event=event)
                attendee.save() 



 #           nameUpdateRequest = {"responseRanges":['Carbon Points Estimator!G4'],
 #                               "includeSpreadsheetInResponse": True,
 #                               "responseIncludeGridData": False,
 #                               "requests": [{"updateCells": {"range":'Carbon Points Estimator!B4:B11',"rows": }}],
 #                               }
 #           result = sheet.batchUpdate(spreadsheetId=settings.SPREADSHEET_ID,body=nameUpdateRequest)

            # redirect to a new URL:
            return HttpResponseRedirect('stations')
        else:
            print('Form not valid, POST')
            return HttpResponseRedirect('/Form not valid on POST/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'carbon_calculator/eventcalculator.html', {'form': form})

class StationsView(generic.ListView):
    model = Station
    template_name = 'carbon_calculator/stations.html'
    context_object_name = 'station_list'

    def __init__(self):
        station_list = estimator.GetStations()
        print('StationsView init, number of stations is '+str(len(station_list)))

        event = Event.objects.get(name=estimator.GetEventName())

        for i in range(len(stationList)):
            station = Station.objects.filter(name=stationList[i]).filter(event=event)
            if (len(station))==0:
                station=Station(name=station_list[i],number=i+1,event=event)
                station.save()

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        event = Event.objects.get(name=estimator.GetEventName())
        return Station.objects.filter(event=event)

class StationDetailView(generic.ListView):
    template_name = 'carbon_calculator/stations-detail.html'
    context_object_name = 'questionList'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(station=station)


def stations(request):
    global next_station
    event_name = estimator.GetEventName()
    event = Event.objects.get(name=event_name)
#    global stationList

    next_station = 1
    stationList = estimator.GetStations()
    print("len(stationList) = "+str(len(stationList)))

    for i in range(len(stationList)):
        station = Station.objects.filter(name=stationList[i]).filter(event=event)
        if (len(station))==0:
            station=Station(name=stationList[i],number=i+1,event=event)
            station.save()

    context = {'stationList':stationList}

    #stationID = 0
    #for station in stationList:
    #    tag = "STATION"+str(stationID)
    ##    stations_context[tag]=station
    #    stationID += 1

    return render(request, 'carbon_calculator/stations.html',context)

def stationdetail(request):
    global next_station
    global stationList

    # no data to proceess
    logger = logging.getLogger(__name__)
    #
    #question_list = []
    responses_list = []
    station_context = {}
    next_station = 1

    stationQuestions = estimator.GetQuestionList(next_station)
    
    if request.method == 'POST':
#        # create a form instance and populate it with data from the request:
        form = StationDetailForm(request.POST)
#        # check whether it's valid:
        if form.is_valid():
#           # process the data in form.cleaned_data as required
#            #likeIt = form.cleaned_data['like_website']
#            #if likeIt:#

            #    logger.info('Thanks for liking the web site')
            #else:
            #    logger.warning('The website likes you anyway')
            # redirect to a new URL:
            logger.info('Going to next station')
            next_station+=1
            return HttpResponseRedirect('stationdetail')
        else:
            logger.error('Form not valid, POST')
            return HttpResponseRedirect('stations-invalid-post')

    # if a GET (or any other method) we'll create a blank form
    else:
        logger.info('Form not submitted yet')  
        print('about to StationDetailForm') 
        #kwargs = {"questions":question_list, "responses":responses_list}     
        form = StationDetailForm(stationQuestions)
        #print(len(form.helper.layout[0]))
        #form.question1.label="A serious question"
        #form.helper.layout[0].append('question1')

    
    #station_context['QUESTION_LIST']=question_list
    print("len(stationList) = "+str(len(stationList)))
    station_context['STATION_TITLE'] = stationList[next_station]
    station_context['station-questions'] = stationQuestions
    next_station += 1
    station_context['form']=form
 
    return render(request, 'carbon_calculator/station-detail.html',station_context)

def example(request):
    # if this is a POST request we need to process the form data
    # Get an instance of a logger
    logger = logging.getLogger(__name__)
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ExampleForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            likeIt = form.cleaned_data['like_website']
            if likeIt:

                logger.info('Thanks for liking the web site')
            else:
                logger.warning('The website likes you anyway')
            # redirect to a new URL:
            return HttpResponseRedirect('stations')
        else:
            logger.error('Form not valid, POST')
            return HttpResponseRedirect('stations-invalid-post')

    # if a GET (or any other method) we'll create a blank form
    else:
        logger.info('Form not submitted yet')        
        form = ExampleForm()


    return render(request, 'carbon_calculator/stations.html', {'form': form})
