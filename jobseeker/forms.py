from django import forms

class LinkedInForm(forms.Form):
    full_name = forms.CharField(label='Your Full Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    linkeInPass = forms.CharField(label='LinkedIn Password')
