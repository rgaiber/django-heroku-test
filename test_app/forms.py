from django import forms

class DestinationSelectionForm(forms.Form):
	destination_name = forms.CharField(label='Destination')

	"""def __str__(self):
		return 'destination: ' + self.destination_name"""