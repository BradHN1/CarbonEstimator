from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Button, HTML, Submit
from crispy_forms.bootstrap import FormActions

from pprint import pprint

question_list = []
responses_list = []
question1 = None
question2 = None

class NameForm(forms.Form):
    firstName = forms.CharField(label='First name', max_length=16, required=False)
    lastName = forms.CharField(label='Last name', max_length=40,required=False)
    email = forms.EmailField(label='E-mail', max_length=50, required=True)
    address = forms.CharField(label='Street', max_length=50, required=False)
    community = forms.CharField(label='Town', max_length=20, required=True)
    team = forms.CharField(label='Team or School', max_length=20, required=True)
    phone = forms.CharField(label='Phone', required=False)
    old_enough = forms.CharField(label='Are you 13 or older?', max_length=3, required=True)

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class StationsForm(forms.Form):
    home_heating = Button('home_heating','Home Heating')
    hot_water = Button('hot_water','Hot Water')
    led_lighting = Button('led_lighting','LED Lighting')
    solar_pv = Button('solar_pv','Solar PV')
    transportation = Button('transportation','Transportation')
    landscaping = Button('landscaping','Landscaping')
    better_eating = Button('better_eating','Low Carbon Diet')
    reduce_reuse = Button('reduce_reuse','Reduce & Reuse')

    def __init__(self, *args, **kwargs):
        super(StationsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-stationsForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                '',   #first arg is the legend of the fieldset
                'home_heating',
                'hot_water',
                'led_lighting',
                'solar_pv',
                'transportation',
                'landscaping',
                'better_eating',
                'reduce_reuse',
            ),
            FormActions(
                Button('startpage', 'Start page'),
                Button('summary', 'Summary'),
            ),
        )

        self.helper.form_action = 'submit_survey'

class StationDetailForm(forms.Form):

    integer1 = forms.IntegerField()
    integer2 = forms.IntegerField()
    integer3 = forms.IntegerField()
    integer4 = forms.IntegerField()
    integer5 = forms.IntegerField()
    integer6 = forms.IntegerField()
    integer7 = forms.IntegerField()
    integer8 = forms.IntegerField()
    integer0 = forms.IntegerField()
    choice1 = forms.ChoiceField()
    choice2 = forms.ChoiceField() 
    choice3 = forms.ChoiceField()
    choice4 = forms.ChoiceField()
    choice5 = forms.ChoiceField() 
    choice6 = forms.ChoiceField()
    choice7 = forms.ChoiceField()
    choice8 = forms.ChoiceField() 
    choice0 = forms.ChoiceField()
    question1 = forms.CharField(required = True,)
    question2 = forms.CharField(label = "Question 2",required = True,)
    question3 = forms.CharField(label = "Question 3",required = True,)
    question4 = forms.CharField(label = "Question 4",required = True,)
    question5 = forms.CharField(label = "Question 5",required = True,)
    question6 = forms.CharField(label = "Question 6",required = True,)
    question7 = forms.CharField(label = "Question 7",required = True,)
    question8 = forms.CharField(label = "Question 8",required = True,)
    question0 = forms.CharField(label = "Question 9",required = True,)        
    print("StationDetailForm - compile time")

    def __init__(self, *args, **kwargs):
        #global question1, question2
        print("StationDetailForm - init")
        #dir(StationDetailForm.question1)
        #StationDetailForm.question1 = forms.CharField(label = "different question",required = True,)
        #pprint(StationDetailForm.question1)
        #question2 = forms.CharField(label = "Question 2",required = True,)

        print("len(args[0])="+str(len(args[0])))
        stationQuestions = args[0]
        pprint(stationQuestions)

        self.helper = FormHelper()
        self.helper.form_id = 'id-stationsDataForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
  
        self.helper.layout = Layout()
        
        # first questions - the current situation
        nq = len(stationQuestions["Current-questions"])
        if (nq>0):
            questionsFieldset = Fieldset( '',   # legend of the fieldset
                    HTML("""<h3>Your current situation:</h3> """))

            for i in range(nq):
                questionsFieldset.append(HTML("<p>"+stationQuestions["Current-questions"][i]+"</p>"))
                response = stationQuestions["Current-responses"][i]
                if response['type']=="NUMBER_BETWEEN":
                    valuerange = (response['values'][0]['userEnteredValue'],
                            response['values'][1]['userEnteredValue'])
                    pprint(valuerange)
                    name = 'integer'+str(i)
                    questionsFieldset.append(name)
                elif response['type']=="ONE_OF_RANGE":
                    valuesString = response['values'][0]['userEnteredValue']
                    if valuesString == "=YesNo":
                        choices = ["yes","no"]
                    name = 'choice'+str(i)
                    questionsFieldset.append(name)
                else:
                    pprint(response['type'])
                    name = 'question'+str(i)
                    questionsFieldset.append(name)

            self.helper.layout.append(questionsFieldset)

        # next questions - the planned situation
        if (len(stationQuestions["Planned-questions"])>0):
            anotherFieldset = Fieldset('',   # legend of the fieldset
                 HTML("""<hr><h3>What you plan to do</h3>"""))
            anotherFieldset.append('question2')
            self.helper.layout.append(anotherFieldset)

        self.helper.layout.append(
            FormActions(
                Button('estimate', 'Estimate'),
                Button('submit', 'Continue'),
            )
        )
        #for i in range(numQuestions):
        #    txt = 'question'+str(i+1)
        #    self.helper.layout[0].append(txt)

        #self.helper.layout[0]

        self.helper.form_action = 'submit_survey'
        super(StationDetailForm, self).__init__()

class ExampleForm(forms.Form):
    like_website = forms.TypedChoiceField(
        label = "Do you like this website?",
        choices = ((1, "Yes"), (0, "No")),
        coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = '1',
        required = True,
    )

    comment1  = forms.CharField(#label = "a label",
        initial = "a comment, some useful HTML informatino",
        widget = forms.Textarea,
        required = False,
    )


    favorite_food = forms.CharField(
        label = "What is your favorite food?",
        max_length = 80,
        required = True,
    )

    favorite_color = forms.CharField(
        label = "What is your favorite color?",
        max_length = 80,
        required = True,
    )

    favorite_number = forms.IntegerField(
        label = "Favorite number",
        required = False,
    )

    notes = forms.CharField(
        label = "Additional notes or feedback",
        required = False,
    )

    def __init__(self, *args, **kwargs):
        super(ExampleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                '',   #first arg is the legend of the fieldset
                'like_website',
                'favorite_number',
                'favorite_color',
                'favorite_food',
                'notes'
            ),
            FormActions(
                Button('estimate', 'Estimate'),
                Button('clear', 'Clear'),
                Submit('save', 'Save'),
            ),
            Button('submit','Continue')
            #ButtonHolder(
            #    Submit('submit', 'Continue', css_class='button white')
            #)
        )

        self.helper.form_action = 'submit_survey'
    
