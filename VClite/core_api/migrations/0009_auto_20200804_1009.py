# Generated by Django 3.0.8 on 2020-08-04 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_api', '0008_customuser_phone_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
