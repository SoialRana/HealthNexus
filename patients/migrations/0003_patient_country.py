# Generated by Django 4.2.5 on 2024-11-16 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_patient_address_patient_date_of_birth_patient_gender_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='country',
            field=models.CharField(default='Bangladesh', max_length=50),
        ),
    ]
