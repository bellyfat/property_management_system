# Generated by Django 2.2.6 on 2019-11-15 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002_auto_20191112_1315'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tenant',
            options={'ordering': ('unit',)},
        ),
    ]