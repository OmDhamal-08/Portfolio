from django import forms
from django.core.validators import EmailValidator

class ContactForm(forms.Form):
    # Hidden honeypot: real visitors never fill this, but many spambots do.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Your Full Name'
        })
    )
    
    email = forms.EmailField(
        max_length=100,
        required=True,
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'your.email@example.com'
        })
    )
    
    subject = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Project Inquiry or General Message'
        })
    )
    
    message = forms.CharField(
        required=True,
        max_length=2000,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Tell me about your project or how I can help you...',
            'rows': 6
        })
    )
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name.strip()) < 2:
            raise forms.ValidationError("Please enter a valid name.")
        return name.strip()

    def clean_subject(self):
        return self.cleaned_data.get('subject', '').strip()

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message.strip()) < 10:
            raise forms.ValidationError("Please enter a message with at least 10 characters.")
        return message.strip()

    def clean_website(self):
        if self.cleaned_data.get('website'):
            raise forms.ValidationError("Invalid submission.")
        return ''
