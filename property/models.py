from __future__ import unicode_literals
from django.utils.dates import MONTHS
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import date
import datetime
from django.core.validators import RegexValidator
from num2words import num2words

# Create your models here.


class Property(models.Model):
    date_added = models.DateField(auto_now_add=True, null=True)
    name = models.CharField(max_length=300, unique=True)
    code = models.CharField(max_length=300, unique=True)
    estate = models.CharField(max_length=300)
    number_of_units = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    number_of_floors =models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):

        return self.name


class Unit(models.Model):
    date_added = models.DateField(auto_now_add=True, null=True)
    property = models.ForeignKey(Property,on_delete=models.CASCADE)
    unit_number = models.CharField(max_length=300)

    floor_CHOICES = [('Ground', 'Ground'),
    ('Parking-Bay', 'Parking-Bay'),]
    for r in range(1,10):
        floor_CHOICES.append((num2words(r,to = 'ordinal'),num2words(r,to = 'ordinal')))
    floor_number =models.CharField(max_length=300,null=True,choices=floor_CHOICES)
    monthly_rent = models.FloatField()
    occupied = models.BooleanField(default=False)
    landlord_assigned = models.BooleanField(default=False)

    class Meta:
        ordering = ('property',)

    def __str__(self):

        return '{} of {}'.format(self.unit_number, self.property)


class Landlord(models.Model):
    date_added = models.DateField(auto_now_add=True, null=True)
    name = models.CharField(max_length=300)
    ID_or_Passport = models.CharField(max_length=300)
    phone_regex = RegexValidator(regex=r'^(?:\+)', message="Phone number must be entered in the format: '+2549999999'. Up to 15 digits allowed.")
    Phone = models.CharField(validators=[phone_regex], max_length=15,null=True)
    unit = models.ForeignKey(Unit, related_name='unit_landlord', on_delete=models.CASCADE)

    def __str__(self):

        return self.name


class Tenant(models.Model):
    date_added = models.DateField(auto_now_add=True, null=True)
    name = models.CharField(max_length=300, unique=True,null=True)
    ID_or_Passport = models.CharField(max_length=300)
    phone_regex = RegexValidator(regex=r'^(?:\+)', message="Phone number must be entered in the format: '+2549999999'. Up to 15 digits allowed.")
    Phone = models.CharField(max_length=15, validators=[phone_regex])
    unit = models.ForeignKey(Unit, related_name='unit_tenant', on_delete=models.CASCADE)
    deposit_paid = models.FloatField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('unit',)

    def __str__(self):
        return '{} from unit {}'.format(self.name, self.unit)


class Transfered_Tenant(models.Model):
    date_added = models.DateField(auto_now_add=True, null=True)
    name = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    old_unit = models.CharField(max_length=200, null=True)
    new_unit = models.ForeignKey(Unit, on_delete=models.CASCADE,related_name='units')
    transfer_date = models.DateField(("Date"), default=date.today)

    def __str__(self):
        return self.name


class Checked_out_Tenant(models.Model):
    date_added = models.DateField(auto_now_add=True, null=True)
    name = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    checked_out_date = models.DateField(("Date"), default=date.today)
    unit_stayed = models.CharField(max_length=200, null=True)

    def __str__(self):

        return self.name


class Rent(models.Model):
    PAYMENT = (
        ('M-PESA', 'M-PESA'),
        ('BANK', 'BANK'),
        ('CASH', 'CASH')
    )
    choices = [(k, v) for k, v in MONTHS.items()]
    month = models.IntegerField(choices=choices, blank=True, null=True,default=datetime.datetime.now().month)
    date_paid = models.DateField(("Date"), default=date.today,null=True,blank=True)
    unit = models.ForeignKey(Unit,on_delete=models.CASCADE,null=True,related_name='unit_rent')
    Amount_paid = models.FloatField()
    Balance = models.FloatField(null=True)
    mode_of_payment = models.CharField(max_length=50, choices=PAYMENT, null=True)
    Reciept_no = models.CharField(max_length=300,blank=True,null=True)
    paid = models.BooleanField(default=True)
    service_charge = models.FloatField(default=0)
    YEAR_CHOICES = []
    for r in range(1980, (datetime.datetime.now().year+20)):
        YEAR_CHOICES.append((r,r))

    year = models.IntegerField(choices=YEAR_CHOICES,
           default=datetime.datetime.now().year,null=True,blank=True)

    def Balance(self):
        if self.Amount_paid < self.unit.monthly_rent:
            self.Balance = self.unit.monthly_rent - self.Amount_paid
        else:
            self.Balance = 0
        return self.Balance

    def __str__(self):

        return 'ksh. {}'.format(self.Amount_paid)



class Expense(models.Model):
    YEAR_CHOICES = []
    for r in range(1980, (datetime.datetime.now().year+20)):
        YEAR_CHOICES.append((r,r))

    year = models.IntegerField(choices=YEAR_CHOICES,
           default=datetime.datetime.now().year,null=True,blank=True)
    choices = [(k, v) for k, v in MONTHS.items()]
    month = models.IntegerField(choices=choices, blank=True, null=True,default=datetime.datetime.now().month)
    property_code = models.ForeignKey(Property,on_delete=models.CASCADE)
    Description = models.TextField(max_length=300)
    Amount = models.FloatField()
    Date = models.DateField(("Date"), default=date.today)

    def __str__(self):
        return '{}'.format(self.Amount)


class Messages(models.Model):
    send_to_all = models.BooleanField(default=False)
    tenant = models.ManyToManyField(Tenant, blank=True)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.message


class Allocated_message(models.Model):
    count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SamatarMessageCounter(models.Model):
    name = models.CharField(max_length=200, null=True)
    total_messages_sent = models.PositiveIntegerField()
