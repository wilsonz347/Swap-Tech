# Generated by Django 5.1.6 on 2025-02-23 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sustainability', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
    ]
