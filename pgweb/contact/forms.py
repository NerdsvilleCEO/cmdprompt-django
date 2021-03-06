from django import forms

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    contact_email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Comment'}))
