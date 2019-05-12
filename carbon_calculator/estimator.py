import os
import pickle

#from django.conf import settings
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from pprint import pprint

class Estimator():
    sheet = None
    eventName = None

    print("Estimator Class - compilation")
    def __init__(self):
        # If modifying these scopes, delete the file token.pickle.
        #SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        # The ID and range of a sample spreadsheet.
        #CARBON_ESTIMATOR_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
        self.spreadsheetId = '1pJJvx83wduDQLHlCtC7SCRgWt49HjwTHbY0RM0EetZs'
        SAMPLE_RANGE_NAME = 'Class Data!A2:E'

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                     'credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        self.sheet = service.spreadsheets()

        result = self.sheet.values().get(spreadsheetId=self.spreadsheetId,
                                range='Carbon Points Estimator!B1').execute()
        values = result.get('values', [])
        self.eventName = values[0][0]

        result = self.sheet.values().get(spreadsheetId=self.spreadsheetId,
                                range='Carbon Points Estimator!F1').execute()
        values = result.get('values', [])
        self.eventDate = values[0][0]

        result = self.sheet.values().get(spreadsheetId=self.spreadsheetId,
                                range='Carbon Points Estimator!F2').execute()
        values = result.get('values', [])
        self.eventLocation = values[0][0]

        result = self.sheet.values().get(spreadsheetId=self.spreadsheetId,
                                range='Carbon Points Estimator!F6').execute()
        values = result.get('values', [])
        self.eventOrganizer = values[0][0]

        result = self.sheet.values().get(spreadsheetId=self.spreadsheetId,
                                range='Carbon Points Estimator!F8').execute()
        values = result.get('values', [])
        self.eventSponsor = values[0][0]

        result = self.sheet.values().get(spreadsheetId=self.spreadsheetId,
                                range='Carbon Points Estimator!A118:A126').execute()
        values = result.get('values', [])
        self.teamList = []
        for i in range(len(values)):
            self.teamList.append(values[i][0])

        pprint(self.teamList)

        self.stationList = []



    def GetInstance(self):
        return self

    def GetEventName(self):
        return self.eventName
    
    def GetEventDate(self):
        return self.eventDate
    
    def GetEventLocation(self):
        return self.eventLocation
    
    def GetEventSponsor(self):
        return self.eventSponsor
    
    def GetEventOrganizer(self):
        return self.eventOrganizer

    def GetTeams(self):
        return self.teamList
    
    def GetStations(self):
        self.stationList = []

        result = self.sheet.values().get(spreadsheetId=self.spreadsheetId,
                                range='Carbon Points Estimator!A13:C116').execute()
        values = result.get('values', [])
        if not values:
            print('No data found')
        else:
            for row in values:
                if len(row)>=3 and len(row[2])>1 and row[2][0]=='T':
                    station = row[0]
                    self.stationList.append(station)
        return self.stationList

    def GetQuestionList(self):
        pass

    def GetQuestionList(self, station):
        response = {}
        current_questions = []
        current_responses = []
        planned_questions = []
        planned_responses = []

        result = self.sheet.values().get(spreadsheetId=self.spreadsheetId,
                                range='Carbon Points Estimator!A13:H116').execute()
        values = result.get('values', [])
        if not values:
            print('No data found')
            return response
       
        request = self.sheet.get(spreadsheetId=self.spreadsheetId,ranges=['Carbon Points Estimator!A13:H116'], includeGridData=True)
        sheet_data = request.execute()
        the_sheet = sheet_data["sheets"][0]
        the_data = the_sheet["data"][0]
        the_rowData = the_data["rowData"]

        #if len(station_list)==0:
        ##    for row in values:
        #        if len(row)>=3 and len(row[2])>1 and row[2][0]=='T':
        #            station = row[0]
        #            station_list.append(station)
        whichRow = 0
        print("station "+str(station))
        for row in values:
            #pprint(row)
            if len(row)>=3 and len(row[2])==1 and int(row[2])==station:
                question = row[0]
                responses = row[1]
                current_questions.append(question)
                #responses_list.append(values)
                #print(question )
                cell_data = the_rowData[whichRow]["values"]
                responseType = cell_data[1]["dataValidation"]["condition"]
                current_responses.append(responseType)

            if len(row)>=6 and len(row[5])==1 and int(row[5])==station:
                question = row[3]
                responses = row[4]
                planned_questions.append(question)
                #responses_list.append(values)
                #print(question )
                cell_data = the_rowData[whichRow]["values"]
                responseType = cell_data[4]["dataValidation"]["condition"]
                planned_responses.append(responseType)

            whichRow += 1

        #pprint(current_questions)
        response["Current-questions"] = current_questions
        response["Current-responses"] = current_responses
        response["Planned-questions"] = planned_questions
        response["Planned-responses"] = planned_responses

        return response
    #def GetQuestionMetadata(self, station):
      #  result = sheet.de

