from django import forms

class getQuery(forms.Form):
	url = forms.CharField(label="url", max_length=200)

class statsSettings(forms.Form):
	limit = forms.IntegerField(label="limit", min_value=2, max_value=750)
	CHOICES = [('1', 'Sort By Hot'),('2', 'Sort By New')]
	sort_type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()