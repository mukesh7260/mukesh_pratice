# Generated by Django 5.0.4 on 2024-12-16 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagesapi', '0002_alter_contact_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='created_at',
            field=models.CharField(default='2024-12-16', max_length=150),
        ),
    ]
