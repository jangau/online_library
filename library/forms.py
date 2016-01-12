from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy
from django.forms.models import ModelForm
from models import Review
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
