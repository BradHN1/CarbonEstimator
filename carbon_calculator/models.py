# from django.db import models
from datetime import datetime
from neomodel import (StructuredNode, StructuredRel, StringProperty,
                      IntegerProperty, BooleanProperty, FloatProperty, EmailProperty,
                      DateTimeProperty, DateProperty, UniqueIdProperty,
                      RelationshipTo, RelationshipFrom, Relationship,
                      ZeroOrMore, ZeroOrOne, OneOrMore)

from django_neomodel import DjangoNode

# Create your models here.
class BaseNode(DjangoNode):
    identifier = UniqueIdProperty()
    name = StringProperty(required=True)
    description = StringProperty()
    alternateName = StringProperty()
    image = StringProperty()
    
    sameAs = Relationship('carbon_calculator.models.BaseNode', 'SAME_AS')

    class Meta:
        app_label = 'carbon_calculator'

class Organization(BaseNode):
    address = StringProperty()
    contact = EmailProperty()

class Event(BaseNode):
    location = StringProperty()
    date = DateTimeProperty()
    organizer = Organization()

class Person(BaseNode):
    firstName = StringProperty()
    lastName = StringProperty()
    email = EmailProperty()
    phone = StringProperty()
    password = StringProperty()
    age_acknowledgment = BooleanProperty()

    teams = RelationshipTo('Team', 'IS_MEMBER', cardinality=ZeroOrMore)

class Volunteer(Person):
    pass

class Attendee(Person):
    carbon_points = FloatProperty()

class Vendor(Person):
    company = StringProperty()
    station = RelationshipTo('Station','HAS_STATION', cardinality=ZeroOrOne)

class Team(BaseNode):
    members = RelationshipTo('Person', 'HAS_MEMBER', cardinality=ZeroOrMore)

class Station(BaseNode):
    subtext = StringProperty()
    description = StringProperty()
    questions = RelationshipTo('Question', 'HAS_QUESTION', cardinality=ZeroOrMore)
 
class Question(BaseNode):
    subtext = StringProperty()
    choices = RelationshipTo('Choice','HAS_CHOICE',cardinality = ZeroOrMore)
    value = FloatProperty()
    units = StringProperty()
    calculatorVariable = RelationshipTo('CalculatorVariable','HAS_VARIABLE',cardinality=ZeroOrOne)

class Choice(BaseNode):
    pass

class Calculation(BaseNode):
    calculatorVariables = RelationshipTo('CalculatorVariable','USES_VARIABLE',cardinality = OneOrMore)
#    calculatorMethod = RelationshipTo()
