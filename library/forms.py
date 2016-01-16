from datetime import datetime, timedelta

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy
from django.forms.models import ModelForm
from models import Review, Borrow, Reserve, Profile, Suggest
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


class EmailInput(forms.EmailInput):
    input_type = 'email'


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


class ReserveForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReserveForm, self).__init__(*args, **kwargs)

        self.fields['period'].required = True

    def clean(self):
        cleaned_data = super(ReserveForm, self).clean()
        cleaned_period = cleaned_data.get('period')
        if cleaned_period:
            if cleaned_period < 1:
                raise forms.ValidationError(u"Can't reserve for less than one day! ", code='invalid')
            if cleaned_period > 14:
                raise forms.ValidationError(u"Can't reserve for more than 14 days! ", code='invalid')
        return cleaned_data

    class Meta:
        model = Reserve
        fields = ['period']
        widgets = {
            'period': NumberInput()
        }


class ProfileForm(forms.ModelForm):

    choices = [('M', 'Male'), ('F', 'Female')]
    gender = ChoiceField(choices=choices, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer))

    class Meta:
        model = Profile
        fields = ['name', 'email', 'address',
                  'birthday', 'gender', 'phone',
                  'card_number', 'card_cvv']
        widgets = {
            'name': forms.TextInput(),
            'email': EmailInput(),
            'birthday': DateInput(),
            'address': forms.TextInput(),
            'phone': forms.NumberInput(),
            'card_number': forms.NumberInput(),
            'card_cvv': forms.NumberInput()
        }


class SuggestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SuggestForm, self).__init__(*args, **kwargs)

        self.fields['title'].required = True
        self.fields['author'].required = True

    class Meta:
        model = Suggest
        fields = ['title', 'author']

        widgets = {
            'title': forms.TextInput(),
            'author': forms.TextInput()
        }