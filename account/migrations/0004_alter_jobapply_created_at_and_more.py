# Generated by Django 5.0.4 on 2024-12-18 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_jobapply_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapply',
            name='created_at',
            field=models.CharField(default='2024-12-18', max_length=150),
        ),
        migrations.AlterField(
            model_name='jobsrequired',
            name='created_at',
            field=models.CharField(default='2024-12-18', max_length=150),
        ),
        migrations.AlterField(
            model_name='telemetrydaa',
            name='date',
            field=models.CharField(default='2024-12-18', max_length=10),
        ),
    ]
