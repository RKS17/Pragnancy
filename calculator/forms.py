from .models import CheckupVisit
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *
from django import forms
from nepali_datetime import date as nepali_date
from nepali_datetime import datetime
from django.db.models.signals import post_save
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm


class PregnancyCalculatorForm(forms.Form):
    last_period_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), label="Date of Last Period"
    )
    pregnancy_weeks = forms.IntegerField(label="Pregnancy Duration in Weeks")


class GestationalAgeForm(forms.Form):
    # LMP date in Nepali BS format
    lmp_date = forms.CharField(
        label='Last Menstrual Period (LMP) Date (BS)',
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g., YYYY-MM-DD', 'class': 'form-control'}),
        required=True
    )
    # Visit date in Nepali BS format
    visit_date = forms.CharField(
        label='Today’s Visit Date (BS)',
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g.,  YYYY-MM-DD', 'class': 'form-control'}),
        required=True
    )


class PregnancyCheckupForm(forms.ModelForm):
    # Custom field for today's Nepali date
    today_date_bs = forms.DateField(
        initial=nepali_date.today(),
        widget=forms.DateInput(
            attrs={'readonly': 'readonly', 'class': 'form-control'}),
        label='आजको मिति (BS)',
        required=False  # If you don't want this to be required
    )

    class Meta:
        model = PregnancyCheckup

        fields = ['patient_name', 'husband_name',
                  'contact_number', 'last_menstrual_period_bs', 'arrival_date', 'ad_arrival_date']
        arrival_date = forms.CharField(
            max_length=10, required=False)  # For Nepali BS date
        ad_arrival_date = forms.DateField(required=False)
        labels = {
            # 'todays_day': 'आजको मिति (BS)',
            'patient_name': 'महिलाको नाम',
            'husband_name': 'पतिको नाम',
            'contact_number': 'संपर्क नम्बर',
            'last_menstrual_period_bs': 'अन्तिम महिनावारी (BS)',
            'lmp_date': forms.DateInput(attrs={'type': 'date'}),
            'iron_per_day': forms.NumberInput(attrs={'step': '0.1'}),
            'calcium_per_day': forms.NumberInput(attrs={'step': '0.1'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Convert the current date to Nepali BS (Bikram Sambat) format
        if not instance.arrival_date:
            # Get today's date in Nepali BS format
            nepali_date = datetime.now().date()
            # Assign the BS date to the arrival_date field
            instance.arrival_date = nepali_date

        if commit:
            instance.save()
        return instance


class CheckupVisitForm(forms.ModelForm):
    class Meta:
        model = CheckupVisit
        fields = [
            'visit_date_bs', 'visit_week',
            'iron_intake', 'calcium_intake',
            'iron_per_day', 'calcium_per_day',  # Include the new fields
            'arrival_time', 'arrival_date',
            'dt_injection', 'intestinal_parasites_medicine'
        ]
        widgets = {
            'visit_date_bs': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            'arrival_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            # Change to DateInput for arrival_date
            'arrival_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'dt_injection': forms.CheckboxInput(),
            'intestinal_parasites_medicine': forms.CheckboxInput(),
            # Add widget for iron_per_day (allowing decimal)
            'iron_per_day': forms.NumberInput(attrs={'step': '0.1'}),
            # Add widget for calcium_per_day (allowing decimal)
            'calcium_per_day': forms.NumberInput(attrs={'step': '0.1'}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
    }))

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'gmail', 'password']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'phone_number', 'gmail', 'profile_image']
