from datetime import datetime, timedelta

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy
from django.forms.models import ModelForm
from models import Review, Borrow, Reserve, Profile, Suggest, Donate
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

    def _post_clean(self):
        super(SuggestForm, self)._post_clean()
        result = [(key, value) for key, value in self.data.iteritems() if key.startswith("resolve") or key.startswith("delete")]
        if len(result):
            del self._errors['title']
            del self._errors['author']

    class Meta:
        model = Suggest
        fields = ['title', 'author']

        widgets = {
            'title': forms.TextInput(),
            'author': forms.TextInput()
        }


class ExtendForm(forms.ModelForm):
    days = CharField(max_length=2, min_length=1, widget=NumberInput())

    class Meta:
        model = Borrow
        fields = ['days']


class DonateForm(forms.ModelForm):

    simage = forms.ImageField(label='')

    def __init__(self, *args, **kwargs):
        super(DonateForm, self).__init__(*args, **kwargs)

        self.fields['title'].required = True
        self.fields['author'].required = True
        self.fields['genre'].required = True
        self.fields['ISBN'].required = True
        self.fields['simage'].required = False

    def clean(self):
        cleaned_data = super(DonateForm, self).clean()
        if not ('accept' in self.data or 'reject' in self.data):
            cleaned_isbn = cleaned_data.get('ISBN')
            if cleaned_isbn:
                if len(cleaned_isbn) != 13 and len(cleaned_isbn) != 10:
                    raise forms.ValidationError(u"Invalid ISBN! ", code='invalid')
        return cleaned_data

    def _post_clean(self):
        super(DonateForm, self)._post_clean()
        result = [(key, value) for key, value in self.data.iteritems() if key.startswith("accept") or key.startswith("reject")]
        if len(result):
            del self._errors['title']
            del self._errors['author']
            del self._errors['genre']
            del self._errors['ISBN']

    class Meta:
        model = Donate
        fields = ['title', 'author', 'genre', 'ISBN', 'simage']

        widgets = {
            'title': forms.TextInput(),
            'author': forms.TextInput(),
            'genre': forms.TextInput(),
            'ISBN': forms.TextInput()
        }
