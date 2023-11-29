# restaurants/forms.py
from django import forms

class PaymentForm(forms.Form):
    phone_number = forms.CharField(max_length=15, label='Phone Number', widget=forms.TextInput(attrs={'class': 'form-control'}))

