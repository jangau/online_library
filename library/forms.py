from datetime import datetime, timedelta

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy
from django.forms.models import ModelForm
from models import Review, Borrow, Reserve
from django.forms.fields import ChoiceField, CharField
from django.utils.safestring import mark_safe


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class ReviewForm(ModelForm):
    choices = [('1', 'Very poor'), ('2', 'Poor'), ('3', 'Not bad'), ('4', 'Good'), ('5', 'Very Good')]
    rating = ChoiceField(choices=choices, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer))
    opinion = CharField(widget=forms.Textarea)

    class Meta:
        fields = ['rating', 'opinion']
        model = Review


class DateInput(forms.DateInput):
    input_type = 'date'


class NumberInput(forms.NumberInput):
    input_type = 'number'

    
class BorrowForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BorrowForm, self).__init__(*args, **kwargs)

        self.fields['date_borrowed'].required = True
        self.fields['date_return'].required = True

        

    def clean(self):
        cleaned_data = super(BorrowForm, self).clean()
        cleaned_date_borrowed = cleaned_data.get('date_borrowed')
        cleaned_date_returned = cleaned_data.get('date_return')
        if cleaned_date_borrowed and cleaned_date_returned:
            if datetime.now().date() > cleaned_date_borrowed:
                raise forms.ValidationError(u"Can't set date in the past! ")
            if cleaned_date_borrowed + timedelta(days=21) <= cleaned_date_returned:
                raise forms.ValidationError(u"Return date must be less than 21 days")
        return cleaned_data

    class Meta:
        model = Borrow
        fields = ['date_borrowed', 'date_return']
        widgets = {
            'date_borrowed': DateInput(),
            'date_return': DateInput()
        }
        

class ReserveForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReserveForm, self).__init__(*args, **kwargs)

        self.fields['period'].required = True

    class Meta:
        model = Reserve
        fields = ['period']
        widgets = {
            'period': NumberInput()
        }