from django import forms
from calculate.models import Email, Applicant


class SwapForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    code = forms.CharField(max_length=6)
    current = forms.CharField(max_length=5, help_text="Please enter your current index.")
    expected = forms.CharField(max_length=5, help_text="Please enter the index you would like.")

    class Meta:
        model = Applicant
        fields = ('name','email','code','current','expected')

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField()
    class Meta:
        model= Email
        fields = ('name','email','message')
