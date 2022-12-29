from django import forms
from django.forms.widgets import DateInput


class ReviewForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    review = forms.CharField(label='Review', widget=forms.Textarea)
    purchased_car = forms.BooleanField(label='Purchased a car', required=False)
    purchase_date = forms.DateField(
        label='Purchase date', widget=DateInput, required=False)
