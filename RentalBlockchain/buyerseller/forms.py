from django import forms
from buyerseller.models import Document

class DocumentForm(forms.Form):
    name = forms.CharField(max_length=100)
    bytecode = forms.FileField()
    abi = forms.FileField()

class CustomForm(forms.Form):  
	def __init__(self, fields, *args, **kwargs):  
		super(CustomForm, self).__init__(*args, **kwargs)  
		for field in fields:
			if field['type'] == 'uint256':  
			    self.fields[field['name']] = forms.IntegerField()  
			elif field['type'] == 'string':  
			    self.fields[field['name']] = forms.CharField(max_length=1000)  
			elif field['type'] == 'boolean': 
			    self.fields[field['name']] = forms.BooleanField(required=False)
			elif field['type'] == 'float':
				self.fields[field['name']] = forms.FloatField()
