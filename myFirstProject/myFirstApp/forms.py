from django import forms
from django.forms import DateField
from django.forms import DateInput, Textarea
from django.conf import settings

from .models import NewsItem, Event


class NewsItemForm(forms.ModelForm):

    class Meta:
        model = NewsItem
        fields = ('title', 'description')


class EventForm(forms.ModelForm):
    start_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=forms.DateInput(attrs={'class': 'datepicker'}))
    end_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=forms.DateInput(attrs={'class': 'datepicker'}))
    
    class Meta:
        model = Event
        fields = ('title', 'description', 'start_date', 'end_date')
