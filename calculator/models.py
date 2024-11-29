from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta
import nepali_datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    gmail = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(
        upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class PregnancyCheckup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    husband_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    last_menstrual_period_bs = models.CharField(max_length=10)
    estimated_due_date_bs = models.CharField(
        max_length=10, blank=True, null=True)
    checkup_dates_bs = models.JSONField(blank=True, null=True)
    total_iron_intake = models.IntegerField(default=0)
    total_calcium_intake = models.IntegerField(default=0)
    arrival_date = models.CharField(
        max_length=10, null=True, blank=True)  # Store Nepali date
    ad_arrival_date = models.DateField(
        null=True, blank=True)
    lmp_date = models.DateField(null=True, blank=True)
    iron_per_day = models.FloatField(null=True, blank=True)
    calcium_per_day = models.FloatField(null=True, blank=True)
    lmp_date_bs = models.CharField(
        max_length=10, null=True, blank=True)  # Nepali Date (BS)
    lmp_date_ad = models.DateField(null=True, blank=True)

    def update_totals(self):
        total_iron = sum(visit.iron_intake for visit in self.visits.all())
        total_calcium = sum(
            visit.calcium_intake for visit in self.visits.all())

        self.total_iron_intake = total_iron
        self.total_calcium_intake = total_calcium
        self.save()

    def save(self, *args, **kwargs):
        # Convert LMP from BS to AD
        lmp_ad = self.bs_to_ad(self.last_menstrual_period_bs)
        due_date_ad = lmp_ad + timedelta(weeks=40)

        # Convert due date to BS
        self.estimated_due_date_bs = self.ad_to_bs(due_date_ad)

        # Generate check-up dates in BS
        self.checkup_dates_bs = self.generate_checkup_schedule(lmp_ad)
        super().save(*args, **kwargs)

    def generate_checkup_schedule(self, lmp_ad):
        """Generate check-up schedule for pregnancy in BS"""
        schedule = []
        checkup_intervals = [
            (12, 12), (16, 16),
            (20, 24),  # Single checkup between weeks 20-24
            (28, 28), (32, 32), (34, 34), (36, 36),
            (38, 40)   # Frequent checkups between weeks 38-40
        ]

        for start_week, end_week in checkup_intervals:
            if start_week == end_week:
                checkup_date_ad = lmp_ad + timedelta(weeks=start_week)
                checkup_date_bs = self.ad_to_bs(checkup_date_ad)
                schedule.append(
                    {'week_range': f"Week {start_week}", 'date': checkup_date_bs})
            else:
                start_date_ad = lmp_ad + timedelta(weeks=start_week)
                end_date_ad = lmp_ad + timedelta(weeks=end_week)
                start_date_bs = self.ad_to_bs(start_date_ad)
                end_date_bs = self.ad_to_bs(end_date_ad)
                schedule.append({
                    'week_range': f"Weeks {start_week}-{end_week}",
                    'date_range': f"{start_date_bs} to {end_date_bs}"
                })
        return schedule

    def bs_to_ad(self, bs_date):
        """Convert BS date to AD date"""
        year, month, day = map(int, bs_date.split('-'))
        return nepali_datetime.date(year, month, day).to_datetime_date()

    def ad_to_bs(self, ad_date):
        """Convert AD date to BS date"""
        bs_date = nepali_datetime.date.from_datetime_date(ad_date)
        return bs_date.strftime('%Y-%m-%d')

    def __str__(self):
        return f"{self.patient_name}'s Pregnancy Schedule"


class CheckupVisit(models.Model):
    patient = models.ForeignKey(
        PregnancyCheckup, on_delete=models.CASCADE, related_name='visits')
    visit_date_bs = models.CharField(max_length=10)  # Date in BS format
    visit_week = models.IntegerField()
    iron_intake = models.IntegerField(default=0)
    calcium_intake = models.IntegerField(default=0)
    arrival_time = models.TimeField(null=True, blank=True)
    arrival_date = models.CharField(max_length=10, null=True, blank=True)
    dt_injection = models.BooleanField(default=False)
    intestinal_parasites_medicine = models.BooleanField(default=False)
    folic_acid = models.BooleanField(default=False)
    total_iron = models.IntegerField(default=0)
    total_calcium = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.patient.patient_name} - Week {self.visit_week} Visit"
