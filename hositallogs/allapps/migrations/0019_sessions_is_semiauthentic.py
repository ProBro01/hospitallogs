# Generated by Django 3.2.8 on 2021-11-18 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allapps', '0018_sessions_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessions',
            name='is_semiauthentic',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
