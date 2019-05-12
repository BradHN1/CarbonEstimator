from django.contrib import admin

# Register your models here.
from .models import Organization, Sponsor, Organizer, Community, Event, Person, Attendee, Station, Question

class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Location',         {'fields': ['location']}),
        ('Date information', {'fields': ['date'], 'classes': ['collapse']}),
        ('Organizer',        {'fields': ['organizer']}),
        ('Sponsor',          {'fields': ['sponsor']}),
    
    ]
    inlines = [] #[ChoiceInline]
    list_display = ('name', 'date')
    list_filter = ['date']
    search_fields = ['name']

class OrganizationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name',            {'fields': ['name']}),
        ('Address',         {'fields': ['address']}),
        ('Description',     {'fields': ['description']}),
        ('Contact',         {'fields': ['contact']}),
    
    ]
    inlines = [] #[ChoiceInline]
    list_display = ('name', 'contact')
    list_filter = []
    search_fields = ['name']

class PersonAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Last Name',               {'fields': ['lastName']}),
        ('First Name',               {'fields': ['firstName']}),
        ('E-mail',               {'fields': ['email']}),       
        ('Phone',               {'fields': ['phone']}),       
        ('Address',         {'fields': ['address']}),
        ('Created', {'fields': ['created'], 'classes': ['collapse']}),
        ('Updated', {'fields': ['updated'], 'classes': ['collapse']}),
    
    ]
    inlines = [] #[ChoiceInline]
    list_display = ('lastName', 'firstName','email')
    list_filter = ['community',]
    search_fields = ['name']

class StationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name',            {'fields': ['name']}),
        ('Number',          {'fields': ['number']}),
        ('Event',           {'fields': ['event']}),
        ('Description',     {'fields': ['description']}),   
    ]
    inlines = []
    list_display = ('name', 'event',)
    list_filter = ['event']
    search_fields = ['name']

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Station',           {'fields': ['station']}),
        ('Question ID',          {'fields': ['questionId']}),
        ('Response Type',          {'fields': ['response_type']}),
        ('Choices',          {'fields': ['choices']}),
    ]
    inlines = []
    list_display = ('question_text', 'station', 'response_type')
    list_filter = ['questionId']
    search_fields = ['question_text']

admin.site.register(Event, EventAdmin)
admin.site.register(Organizer, OrganizationAdmin)
admin.site.register(Sponsor, OrganizationAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Attendee, PersonAdmin)
admin.site.register(Station, StationAdmin)
admin.site.register(Question, QuestionAdmin)
