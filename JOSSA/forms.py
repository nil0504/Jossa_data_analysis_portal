from django import forms

class Userform(forms.Form):
    email=forms.EmailField(label="Email",widget=forms.TextInput(attrs={'class':"form-control"}))
    password=forms.CharField(label="Email",widget=forms.TextInput(attrs={'class':"form-control"}))
    