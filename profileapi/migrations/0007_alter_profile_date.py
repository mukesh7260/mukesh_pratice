# Generated by Django 5.0.4 on 2025-01-03 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileapi', '0006_alter_profile_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date',
            field=models.CharField(default='2025-01-03', max_length=10),
        ),
    ]
