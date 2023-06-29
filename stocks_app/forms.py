
from django import forms
from .models import Stock

class StockForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ["ticker"]
    	#your_name = forms.CharField(label="Your name", max_length=100)