from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from .estimator import Estimator

#from django.views import generic
import logging

from .forms import NameForm, ContactForm, ExampleForm,StationDetailForm
from .models import Station

event_name = 'Cooler Communities Event Calculator'
stationList = []
next_station = 1
estimator = Estimator()

# Create your views here.
def index(request):
      
    event_name = estimator.GetEventName()
    welcome_context = {'EVENT_NAME':event_name}
    return render(request, 'carbon_calculator/welcome.html', welcome_context)
 
def about(request):
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

def stations(request):
    global next_station
    global stationList

    stations_context = {}
    next_station = 1
    stationList = estimator.GetStations()
    print("len(stationList) = "+str(len(stationList)))

    stationID = 0
    for station in stationList:
        tag = "STATION"+str(stationID)
        stations_context[tag]=station
        stationID += 1

    return render(request, 'carbon_calculator/stations.html',stations_context)

def stationdetail(request):
    global next_station
    global stationList

    # no data to proceess
    logger = logging.getLogger(__name__)
    #
    #question_list = []
    responses_list = []
    station_context = {}
    next_station = 0

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
