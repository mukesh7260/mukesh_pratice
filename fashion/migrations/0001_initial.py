<<<<<<< HEAD
# Generated by Django 5.0.4 on 2024-12-11 07:24
=======
# Generated by Django 5.0.4 on 2025-01-06 10:53
>>>>>>> 8a72e49cd22e840587db7c1423cb1ca18330101d

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fashion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_title', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('Men', 'Men'), ('Women', 'Women'), ('Kids', 'Kids')], max_length=10)),
                ('description', models.TextField()),
                ('images', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
