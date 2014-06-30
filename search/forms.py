from django import forms

class SearchForm(forms.Form):
    q = forms.CharField(label='Search Referrals', max_length=100)
