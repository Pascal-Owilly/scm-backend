# forms.py

from django import forms

class SlaughterForm(forms.Form):
    breeds_to_slaughter = forms.ModelMultipleChoiceField(queryset=BreaderTrade.objects.all(), widget=forms.CheckboxSelectMultiple)
