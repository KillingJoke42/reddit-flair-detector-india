# django's form render library
from django import forms

# Form to get the URL from the user for prediction
class getQuery(forms.Form):
	url = forms.CharField(label="url", max_length=200)

# Get the Post limit and the sorting type from the user for statistics
class statsSettings(forms.Form):
	limit = forms.IntegerField(label="limit", min_value=2, max_value=750)
	CHOICES = [('1', 'Sort By Hot'),('2', 'Sort By New')]
	sort_type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)