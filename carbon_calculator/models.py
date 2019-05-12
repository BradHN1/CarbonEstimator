# from django.db import models
from datetime import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    contact = models.EmailField()

class Sponsor(Organization):
    pass

class Organizer(Organization):
    pass

class Community(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length = 80)
    location = models.CharField(max_length = 80)
    date = models.DateTimeField()
    organizer = models.ForeignKey(Organizer, on_delete=models.PROTECT)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.PROTECT)

class Person(models.Model):
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)    
    firstName = models.CharField(max_length = 20)
    lastName = models.CharField(max_length = 20)
    address = models.CharField(max_length = 50, default = "")
    community = models.CharField(max_length = 30)
    email = models.EmailField()
    phone = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    age_acknowledgment = models.BooleanField()

class Team(models.Model):
    name = models.CharField(max_length=40)
    members = models.IntegerField(default=0)
    carbon_points = models.FloatField(default=0.0)
    dollar_savings = models.FloatField(default=0.0)

#    teams = RelationshipTo('Team', 'IS_MEMBER', cardinality=ZeroOrMore)


#class Volunteer(Person):
 #   affiliation = Organization()

class Attendee(Person):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    carbon_points = models.FloatField(default=0.0)
    dollar_savings = models.FloatField(default=0.0)

#class Vendor(Person)
#    company = StringProperty()
#    station = RelationshipTo('Station','HAS_STATION', cardinality=ZeroOrOne)

#class Team(models.Model):
#    members = RelationshipTo('Person', 'HAS_MEMBER', cardinality=ZeroOrMore)

class Station(models.Model):
    name = models.CharField(max_length = 20)
    number = models.IntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.CharField(max_length = 200)
#    questions = RelationshipTo('Question', 'HAS_QUESTION', cardinality=ZeroOrMore)
    def __str__(self):
        return self.name
 
class Question(models.Model):
    question_text = models.CharField(max_length=20)
    description = models.CharField(max_length= 200)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    questionId = models.IntegerField(default = 0)
    response_type = models.CharField(max_length=10)
    choices = models.CharField(max_length=40)
#    calculatorVariable = RelationshipTo('CalculatorVariable','HAS_VARIABLE',cardinality=ZeroOrOne)
    def __str__(self):
        return self.question_text


    #population = models.IntegerField()
    #members = model.IntegerField()

#class Choice(models.Model):
#    question = models.ForeignKey(Question, on_delete=models.CASCADE)
#    choice_text = models.CharField(max_length=200)
#    def __str__(self):
#        return self.choice_text

#class Calculation(models.Model):
#    calculatorVariables = RelationshipTo('CalculatorVariable','USES_VARIABLE',cardinality = OneOrMore)
#    calculatorMethod = RelationshipTo()
