from django.contrib import admin

# Register your models here.
from .models import Organization, Sponsor, Organizer, Community, Event, Person, Attendee, Station, Question

#class ChoiceInline(admin.TabularInline):
#    model = Choice
#    extra = 3

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
        ('Community',        {'fields': ['community']}),
        ('Sponsor',          {'fields': ['sponsor']}),
        ('Created', {'fields': ['created'], 'classes': ['collapse']}),
        ('Updated', {'fields': ['updated'], 'classes': ['collapse']}),
    
    ]
    inlines = [] #[ChoiceInline]
    list_display = ('lastName', 'firstName','email')
    list_filter = ['community',]
    search_fields = ['name']

#class QuestionAdmin(admin.ModelAdmin):
#    fieldsets = [
##        (None,               {'fields': ['question_text']}),
#        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#    ]
#    inlines = [ChoiceInline]
#    list_display = ('question_text', 'pub_date', 'was_published_recently')
#    list_filter = ['pub_date']
#   search_fields = ['question_text']

admin.site.register(Event, EventAdmin)
admin.site.register(Organizer, OrganizationAdmin)
admin.site.register(Sponsor, OrganizationAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Attendee, PersonAdmin)
