from django import forms


class VolumeDetectorForm(forms.Form):
    url = forms.CharField(label='URL', widget=forms.TextInput(attrs={
                          'class': 'form-control', 'value': 'http://radiocentral.ice.infomaniak.ch/radiocentral-128.mp3'}))
    threshold = forms.IntegerField(label='Threshold', widget=forms.NumberInput(
        attrs={'class': 'form-control', 'value': -30}))
    duration = forms.IntegerField(label='Duration', widget=forms.NumberInput(
        attrs={'class': 'form-control', 'value': 10}))
