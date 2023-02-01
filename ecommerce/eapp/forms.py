from django import forms

class ulogform(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(max_length=25)

class regform(forms.Form):
    name=forms.CharField(max_length=20)
    email=forms.EmailField()
    password=forms.CharField(max_length=25)

class shopform(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(max_length=25)


class shopregform(forms.Form):
    sname=forms.CharField(max_length=20)
    semail=forms.EmailField()
    spassword=forms.CharField(max_length=25)

class uploadform(forms.Form):
    name=forms.CharField(max_length=25)
    image=forms.ImageField()
    price=forms.IntegerField()
    description=forms.CharField(max_length=30)