# Generated by Django 3.1.4 on 2020-12-31 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_profile_idc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='idc',
            field=models.IntegerField(default=0),
        ),
    ]