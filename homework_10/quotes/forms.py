from datetime import date

from django.forms import ModelForm, CharField, TextInput, DateField, DateTimeInput, SelectDateWidget

from .models import Tag, Quote, Author




class TagForm(ModelForm):

    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())
    
    class Meta:
        model = Tag
        fields = ['name']
        
class QuoteForm(ModelForm):

    # name = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    description = CharField(min_length=10, max_length=150, required=True, widget=TextInput())

    class Meta:
        model = Quote
        exclude = ['author']
        exclude = ['tags']
        fields = ['description']


class AuthorForm(ModelForm):

    full_name = CharField(min_length=5, max_length=100, required=True, widget=TextInput())
    born_date = DateField(widget=SelectDateWidget(years=range(1700, int(date.today().strftime("%Y"))+1),empty_label=("Select year","Select month","Select day")))
    born_location = CharField(min_length=6, max_length=255, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['full_name', 'born_date', 'born_location']
