from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class':'input input-bordered','placeholder':'جستجو'}) )
 