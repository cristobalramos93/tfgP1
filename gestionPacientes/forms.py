from django import forms

class SignUpForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Username'}))
    firstName = forms.CharField(label='First Name', max_length=20,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Firstname'}))
    lastName = forms.CharField(label='Last Name', max_length=20,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter LastName'}))
    email = forms.CharField(label='Email', max_length=220,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Email','type':'email'}))
    password = forms.CharField(label="Confirm Password", max_length=20,widget=forms.TextInput(attrs={'class': 'form-control','type':'password','placeholder':'Enter Password'}))
    conPassword = forms.CharField(label="Confirm Password", max_length=20,widget=forms.TextInput(attrs={'class': 'form-control','type':'password','placeholder':'Confirm Password'}))