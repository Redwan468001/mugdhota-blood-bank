from django import forms
from .models import User, Donner, Location, Contact, BloodInfoAddProblem
from django.contrib.auth.forms import UserCreationForm


class PersonCreationForm(forms.ModelForm):

    class Meta:
        model = Donner
        fields = ['name', 'bloodgroups', 'division', 'location', 'city', 'donation_date', 'phone']

        widgets = {
            'donation_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'name': 'Display Name'
        }


    def clean(self):
        cleaned_date = super().clean()
        name = cleaned_date.get('name', None)
        bloodgroups = cleaned_date.get('bloodgroups', None)
        location = cleaned_date.get('location', None)
        phone = cleaned_date.get('phone', None)

        #if Donner.objects.filter(phone=phone).exists():
         #   self.add_error('You are not allowed here')

        if phone and len(str(phone)) != 11:
            self.add_error('phone', 'Aadhaar must be 12 digit')
            
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.none()

        if 'division' in self.data:
            try:
                division_id = int(self.data.get('division'))
                self.fields['location'].queryset = Location.objects.filter(division_id=division_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
            

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'question']


class BiapForm(forms.ModelForm):

    class Meta:
        model = BloodInfoAddProblem
        fields = ['name', 'email', 'phone', 'question']


# User Creation form
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'phone', 'email', 'password1', 'password2']


# User update form
class EditProfile(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'name', 'phone', 'bio', 'bloodgroups', 'avatar']


#User uploaded donner update form
class UserUploadDonerUpdareForm(forms.ModelForm):

    class Meta:
        model = Donner
        fields = ['division', 'location', 'city', 'donation_date', 'phone']

        widgets = {
            'donation_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'division': 'বিভাগঃ', 'location': 'জেলাঃ', 'city': 'উপজেলা/থানাঃ', 'phone': 'মোবাইলঃ', 'donation_date': 'সর্বশেষ রক্তদানঃ'
        }


    def clean(self):
        cleaned_date = super().clean()
        name = cleaned_date.get('name', None)
        bloodgroups = cleaned_date.get('bloodgroups', None)
        location = cleaned_date.get('location', None)
        phone = cleaned_date.get('phone', None)

        #if Donner.objects.filter(phone=phone).exists():
         #   self.add_error('You are not allowed here')

        if phone and len(str(phone)) != 11:
            self.add_error('phone', 'Aadhaar must be 12 digit')
            
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.all()

        if 'division' in self.data:
            try:
                division_id = int(self.data.get('division'))
                self.fields['location'].queryset = Location.objects.filter(division_id=division_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
