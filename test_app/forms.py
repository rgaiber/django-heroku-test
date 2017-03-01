from django import forms

class DestinationSelectionForm(forms.Form):
    destination_name = forms.CharField(label='Destination')