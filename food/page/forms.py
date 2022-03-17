from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email')


class FoodForm(forms.Form):
    food = forms.CharField(label='Food', max_length=100)
    user_id = forms.IntegerField(label='user_id')