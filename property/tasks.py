import africastalking
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from .credentials import USERNAME, APIKEY
from property.models import Allocated_message, Tenant
from django.shortcuts import render,HttpResponse
from background_task import background
from datetime import timedelta
import datetime


username = USERNAME
api_key = APIKEY
africastalking.initialize(username, api_key)



# Create your views here.
@background(schedule=datetime.datetime(2019, 12, 5, 8, 30))
def hello():
    sms = africastalking.SMS
    allocated_model = Allocated_message.objects.get(name='admin')
    allocated_messages = allocated_model.count
    message = 'Hello valued Tenant, this is to remind you to pay the rent early enough'
    message_len = len(message)
    tenants = Tenant.objects.filter(active=True)
    if message_len <= 144:
        mes_count = 1
    elif message_len <= 304:
        mes_count = 2
    elif message_len <= 464:
        mes_count = 3
    elif message_len <= 624:
        mes_count = 4
    elif message_len <= 784:
        mes_count = 5
    if mes_count < allocated_messages:
        for ten in tenants:
            phone_number = ten.Phone
            sms.send(message, [phone_number], 'softsearch')
    else:
        pass



@periodic_task(run_every=(crontab(minute='*/1')), name="some_task", ignore_result=True)
def some_task():
    sms = africastalking.SMS
    allocated_model = Allocated_message.objects.get(name='admin')
    allocated_messages = allocated_model.count
    message = 'Hello valued Tenant, this is to remind you to pay the rent early enough'
    message_len = len(message)
    tenants = Tenant.objects.filter(active=True)
    if message_len <= 144:
        mes_count = 1
    elif message_len <= 304:
        mes_count = 2
    elif message_len <= 464:
        mes_count = 3
    elif message_len <= 624:
        mes_count = 4
    elif message_len <= 784:
        mes_count = 5
    if mes_count < allocated_messages:
        for ten in tenants:
            phone_number = ten.Phone
            sms.send(message, [phone_number], 'softsearch')
    else:
        pass
