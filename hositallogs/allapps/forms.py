from django import forms

class loginform(forms.Form):
    username = forms.CharField(max_length=10, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)