# Generated by Django 4.2.16 on 2024-11-03 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='code',
            field=models.CharField(max_length=4),
        ),
    ]